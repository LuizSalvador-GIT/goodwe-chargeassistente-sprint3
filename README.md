# EV Challenge — GoodWe · Sprint 03

Refatoração conversacional em LangChain LCEL para o Challenge de mobilidade elétrica
da FIAP × GoodWe Brasil.

## Preparação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen3:4b-instruct
```

O desenvolvimento local usa `qwen3:4b-instruct`. Para a avaliação exigida, use
`gpt-oss:120b-cloud` ou configure `OLLAMA_BASE_URL` para um servidor remoto que tenha
`gpt-oss:120b`; o arquivo local do modelo tem 65 GB e não cabe nesta máquina.

## Executar o chatbot

```bash
python app.py --session demonstracao
```

Use a mesma sessão por três ou mais turnos para demonstrar a memória.

Para preservar a interface Streamlit do projeto anterior:

```bash
streamlit run streamlit_app.py
```

## Publicar no Streamlit Community Cloud

1. Envie este projeto para um repositório GitHub público.
2. Em `share.streamlit.io`, crie um app usando `streamlit_app.py`.
3. Em **Advanced settings > Secrets**, cadastre:

```toml
LLM_PROVIDER = "nvidia"
NVIDIA_API_KEY = "sua-chave-nvapi"
NVIDIA_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"
```

Nunca salve o valor real da chave no GitHub. Localmente, mantenha
`LLM_PROVIDER=ollama` no `.env` para usar o Qwen instalado.

Se o endpoint NVIDIA estiver indisponível, use o roteador gratuito do OpenRouter:

```toml
LLM_PROVIDER = "openrouter"
OPENROUTER_API_KEY = "sua-chave-openrouter"
OPENROUTER_MODEL = "nvidia/nemotron-3.5-lightning:free"
```

## Structured output

O schema `ConsultaRecarga` está em `src/schemas/consulta_recarga.py`; a chain correspondente
é criada por `build_structured_chain()`.

## Avaliações

```bash
python -m evals.run_evals --variant legacy
python -m evals.run_evals --variant sprint3
python -m evals.run_structured_evals --model qwen3:4b-instruct
```

Os resultados são salvos em `evals/legacy_results.json` e `evals/sprint3_results.json`.
O avaliador mede decisão de segurança, qualidade por critérios verificáveis, tokens e
latência. A saída estruturada é validada separadamente pelo mesmo comando da Sprint 03.

## Código anterior

O projeto anterior está documentado em `docs/baseline_sprints_1_2.md`. `chat.py` e
`bot.py` são experimentos locais separados; o ChargeAssistente começa em `app.py` ou
`streamlit_app.py`.
