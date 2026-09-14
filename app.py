import argparse

from src.chain import build_chatbot
from src.guardrails import moderate_input


def main() -> None:
    parser = argparse.ArgumentParser(description="Chatbot EV Challenge — GoodWe")
    parser.add_argument("--session", default="demo", help="identificador da sessão")
    parser.add_argument("--model", default=None, help="modelo instalado no Ollama")
    args = parser.parse_args()

    chatbot = build_chatbot(model=args.model)
    config = {"configurable": {"session_id": args.session}}
    print("Chatbot GoodWe. Digite /sair para encerrar.\n")

    while True:
        try:
            question = input("você> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo.")
            break
        if question.lower() in {"/sair", "/exit", "/quit"}:
            break
        if not question:
            continue

        decision = moderate_input(question)
        if not decision.allowed:
            print(f"bot> {decision.response}")
            continue

        try:
            response = chatbot.invoke({"input": question}, config=config)
            print(f"bot> {response}")
        except Exception as exc:
            print(f"Erro ao consultar o Ollama: {exc}")
            print("Confirme se o Ollama está aberto e se o modelo foi baixado.")


if __name__ == "__main__":
    main()
