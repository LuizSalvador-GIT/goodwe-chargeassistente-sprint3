import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    ollama_model: str = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    memory_token_limit: int = int(os.getenv("MEMORY_TOKEN_LIMIT", "1800"))
    temperature: float = 0.2
    top_p: float = 0.9
    max_tokens: int = 512


settings = Settings()
