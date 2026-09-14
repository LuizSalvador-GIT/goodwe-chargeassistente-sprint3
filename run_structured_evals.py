import argparse
import json
import statistics
import time
from pathlib import Path

from src.chain import build_structured_chain
from src.config import settings

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    {
        "input": "O carregador ev-17 está carregando a 7,4 kW e consumiu 12,5 kWh. Valor R$ 18,90.",
        "expected": {"carregador_id": "EV-17", "estado": "carregando", "potencia_kw": 7.4, "energia_kwh": 12.5, "valor_brl": 18.9},
    },
    {
        "input": "O ponto gw-02 está indisponível. Ainda não temos potência, energia nem valor.",
        "expected": {"carregador_id": "GW-02", "estado": "indisponivel", "potencia_kw": None, "energia_kwh": None, "valor_brl": None},
    },
    {
        "input": "Carregador A-9 disponível, potência de 22 kW.",
        "expected": {"carregador_id": "A-9", "estado": "disponivel", "potencia_kw": 22.0, "energia_kwh": None, "valor_brl": None},
    },
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=None)
    args = parser.parse_args()
    model = args.model or settings.ollama_model
    chain = build_structured_chain(model=model)
    results = []
    for case in CASES:
        started = time.perf_counter()
        try:
            parsed = chain.invoke({"input": case["input"]}).model_dump(mode="json")
            checks = {key: parsed[key] == value for key, value in case["expected"].items()}
            error = None
        except Exception as exc:
            parsed, checks, error = None, {}, str(exc)
        results.append({**case, "output": parsed, "checks": checks, "passed": bool(checks) and all(checks.values()), "error": error, "latency_ms": round((time.perf_counter() - started) * 1000, 2)})
    payload = {
        "model": model,
        "summary": {
            "cases": len(results),
            "accuracy": sum(item["passed"] for item in results) / len(results),
            "mean_latency_ms": round(statistics.mean(item["latency_ms"] for item in results), 2),
        },
        "results": results,
    }
    path = ROOT / "evals" / "structured_results.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Resultados gravados em {path}")


if __name__ == "__main__":
    main()
