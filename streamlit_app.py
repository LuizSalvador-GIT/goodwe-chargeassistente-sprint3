import uuid

import streamlit as st

from src.chain import build_chatbot
from src.guardrails import moderate_input

st.set_page_config(page_title="ChargeAssistente — GoodWe", page_icon="⚡")
st.title("⚡ ChargeAssistente")
st.caption("GoodWe EV ChargeOps — suporte ao morador")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Olá! Posso ajudar com recarga, agendamento, rateio e suporte básico aos eletropostos do condomínio.",
    }]
if "chatbot" not in st.session_state:
    st.session_state.chatbot = build_chatbot()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Digite sua dúvida sobre os carregadores…"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    decision = moderate_input(question)
    if decision.allowed:
        try:
            answer = st.session_state.chatbot.invoke(
                {"input": question},
                config={"configurable": {"session_id": st.session_state.session_id}},
            )
        except Exception as exc:
            answer = f"Não consegui consultar o modelo local. Verifique o Ollama. Detalhe: {exc}"
    else:
        answer = decision.response

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
