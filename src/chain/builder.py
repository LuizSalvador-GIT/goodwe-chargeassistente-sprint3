from pathlib import Path

from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

from src.config import settings
from src.schemas import ConsultaRecarga
from src.token_metrics import get_token_ids

from .memoria import SessionMemoryStore

ROOT = Path(__file__).resolve().parents[2]


def _load_prompt(version: str = "v2") -> str:
    return (ROOT / "prompts" / f"system_prompt_{version}.md").read_text(encoding="utf-8")


def build_llm(model: str | None = None) -> ChatOllama:
    return ChatOllama(
        model=model or settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=settings.temperature,
        top_p=settings.top_p,
        num_predict=settings.max_tokens,
        reasoning=False,
        custom_get_token_ids=get_token_ids,
    )


def build_chatbot(model: str | None = None, prompt_version: str = "v3"):
    selected_model = model or settings.ollama_model
    llm = build_llm(selected_model)
    system_prompt = _load_prompt(prompt_version)
    human_template = "{input}"
    if selected_model.lower().startswith("qwen3"):
        human_template = "{input}\n\n/no_think"
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", human_template),
    ])
    chain = prompt | llm | StrOutputParser()
    sessions = SessionMemoryStore(llm, settings.memory_token_limit)
    return RunnableWithMessageHistory(
        chain,
        sessions.get,
        input_messages_key="input",
        history_messages_key="history",
    )


def build_structured_chain(model: str | None = None):
    selected_model = model or settings.ollama_model
    parser = PydanticOutputParser(pydantic_object=ConsultaRecarga)
    system_prompt = _load_prompt("v3")
    no_think = "\n\n/no_think" if selected_model.lower().startswith("qwen3") else ""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Extraia os dados da consulta abaixo. Use desconhecido ou null quando o dado não existir.\n\n{format_instructions}\n\nConsulta: {input}{no_think}"),
    ]).partial(format_instructions=parser.get_format_instructions(), no_think=no_think)
    return prompt | build_llm(selected_model) | parser
