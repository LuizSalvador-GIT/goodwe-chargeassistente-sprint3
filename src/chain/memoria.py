from collections.abc import Sequence

from langchain_classic.memory import ConversationTokenBufferMemory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


class TokenBufferHistory(BaseChatMessageHistory):
    """Adapta ConversationTokenBufferMemory ao RunnableWithMessageHistory."""

    def __init__(self, llm, max_token_limit: int):
        self.memory = ConversationTokenBufferMemory(
            llm=llm,
            max_token_limit=max_token_limit,
            memory_key="history",
            return_messages=True,
        )

    @property
    def messages(self) -> list[BaseMessage]:
        return self.memory.chat_memory.messages

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        pending = list(messages)
        while len(pending) >= 2 and isinstance(pending[0], HumanMessage) and isinstance(pending[1], AIMessage):
            human, assistant = pending.pop(0), pending.pop(0)
            self.memory.save_context({"input": human.content}, {"output": assistant.content})
        for message in pending:
            self.memory.chat_memory.add_message(message)

    def clear(self) -> None:
        self.memory.clear()


class SessionMemoryStore:
    def __init__(self, llm, max_token_limit: int):
        self.llm = llm
        self.max_token_limit = max_token_limit
        self._sessions: dict[str, TokenBufferHistory] = {}

    def get(self, session_id: str) -> TokenBufferHistory:
        if session_id not in self._sessions:
            self._sessions[session_id] = TokenBufferHistory(self.llm, self.max_token_limit)
        return self._sessions[session_id]
