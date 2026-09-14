"""Baseline manual reconstruída para comparação com as Sprints 1/2."""

from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from src.chain.builder import build_llm

ROOT = Path(__file__).resolve().parents[1]


class LegacyChatbot:
    """Monta mensagens manualmente, sem LCEL, memória ou parser."""

    def __init__(self, model: str | None = None):
        self.llm = build_llm(model)
        self.system_prompt = (ROOT / "prompts" / "system_prompt_v2.md").read_text(encoding="utf-8")

    def invoke(self, user_input: str) -> str:
        response = self.llm.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_input),
        ])
        return str(response.content)
