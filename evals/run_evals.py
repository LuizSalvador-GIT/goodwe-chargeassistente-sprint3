import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chain import build_chatbot
from src.config import settings
from src.guardrails import moderate_input
from src.legacy import LegacyChatbot
from src.token_metrics import count_tokens, prompt_token_report


def quality_check(case: dict, output: str, outcome: str) -> tuple[bool, list[str]]:
    if outcome != case["expected"]:
        return False, [f"decisão esperada: {case['expected']}"]
    normalized = output.lower()
    failures = []
    required = case.get("must_include_any", [])
    if required and not any(term.lower() in normalized for term in required):
        failures.append("nenhum termo obrigatório encontrado")
    forbidden = [term for term in case.get("must_not_include", []) if term.lower() in normalized]
    if forbidden:
        failures.append("conteúdo proibido: " + ", ".join(forbidden))
    return not failures, failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=["legacy", "sprint3"], default="sprint3")
    parser.add_argument("--provider", choices=["ollama", "nvidia", "openrouter"], default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    cases = json.loads((ROOT / "evals" / "eval_set.json").read_text(encoding="utf-8"))
    provider = args.provider or settings.llm_provider
    provider_models = {
        "ollama": settings.ollama_model,
        "nvidia": settings.nvidia_model,
        "openrouter": settings.openrouter_model,
    }
    selected_model = args.model or provider_models[provider]
    chatbot = (
        build_chatbot(model=selected_model, provider=provider)
        if args.variant == "sprint3"
        else LegacyChatbot(model=selected_model)
    )
    results = []

    for case in cases:
        started = time.perf_counter()
        decision = moderate_input(case["input"]) if args.variant == "sprint3" else None
        if decision is None or decision.allowed:
            if args.variant == "sprint3":
                output = chatbot.invoke(
                    {"input": case["input"]},
                    config={"configurable": {"session_id": f"eval-{case['id']}"}},
                )
            else:
                output = chatbot.invoke(case["input"])
            outcome = "allowed"
        else:
            output = decision.response or ""
            outcome = "blocked"
        passed, quality_failures = quality_check(case, output, outcome)
        results.append({
            **case,
            "outcome": outcome,
            "passed": passed,
            "quality_failures": quality_failures,
            "latency_ms": round((time.perf_counter() - started) * 1000, 2),
            "input_tokens": count_tokens(case["input"]),
            "output_tokens": count_tokens(output),
            "output": output,
        })

    payload = {
        "variant": args.variant,
        "provider": provider,
        "model": selected_model,
        "prompt_tokens": prompt_token_report(ROOT / "prompts"),
        "summary": {
            "cases": len(results),
            "pass_rate": sum(item["passed"] for item in results) / len(results),
            "mean_latency_ms": round(statistics.mean(item["latency_ms"] for item in results), 2),
            "mean_input_tokens": round(statistics.mean(item["input_tokens"] for item in results), 2),
            "mean_output_tokens": round(statistics.mean(item["output_tokens"] for item in results), 2),
        },
        "results": results,
    }
    default_name = "sprint3_results.json" if args.variant == "sprint3" else "legacy_results.json"
    output_path = ROOT / "evals" / (args.output or default_name)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Resultados gravados em {output_path}")


if __name__ == "__main__":
    main()
