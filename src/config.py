import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama").lower()
    ollama_model: str = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    nvidia_api_key: str | None = os.getenv("NVIDIA_API_KEY")
    nvidia_model: str = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3.5-lightning-30b-a3b")
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3.5-lightning:free")
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    memory_token_limit: int = int(os.getenv("MEMORY_TOKEN_LIMIT", "1800"))
    temperature: float = 0.2
    top_p: float = 0.9
    max_tokens: int = 512


settings = Settings()
