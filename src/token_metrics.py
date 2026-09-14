from pathlib import Path

import tiktoken


def get_token_ids(text: str) -> list[int]:
    """Tokenização única usada nas métricas e no limite da memória."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return encoding.encode(text)


def count_tokens(text: str) -> int:
    return len(get_token_ids(text))


def prompt_token_report(prompts_dir: Path) -> dict[str, int]:
    return {
        path.stem: count_tokens(path.read_text(encoding="utf-8"))
        for path in sorted(prompts_dir.glob("system_prompt_v*.md"))
    }
