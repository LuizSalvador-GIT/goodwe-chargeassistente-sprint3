# EV Challenge - GoodWe - Sprint 03

Evolução do ChargeAssistente das Sprints 1 e 2 para uma arquitetura conversacional
com LangChain LCEL, memória por sessão, structured output Pydantic v2, context
engineering e guardrails.

## Demonstração pública

- Aplicação: <https://goodwe-chargeassistente-sprint3-3nerteh7va8qna8g8gr9rz.streamlit.app/>
- Relatório: [`docs/relatorio_evolucao.pdf`](docs/relatorio_evolucao.pdf)
- Integrantes: [`integrantes.txt`](integrantes.txt)

## Funcionalidades da Sprint 03

- Chain LCEL: `ChatPromptTemplate | ChatOllama/ChatOpenAI | parser`.
- Memória por sessão com `RunnableWithMessageHistory` e
  `ConversationTokenBufferMemory`, limitada a 1.800 tokens.
- Structured output com o schema `ConsultaRecarga` e `field_validator`.
- System prompts versionados com XML tagging e contagem de tokens via `tiktoken`.
- Guardrails para escopo GoodWe, prompt injection, risco elétrico e orientação
  jurídica ou financeira.
- Eval reproduzível do fluxo legado e da Sprint 03.
- Provedores configuráveis: Ollama, NVIDIA API e OpenRouter.

## Executar localmente

Requisitos: Python 3.12 ou superior e Ollama instalado.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen3:4b-instruct
cp .env.example .env
```

No arquivo `.env`, mantenha:

```dotenv
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3:4b-instruct
OLLAMA_BASE_URL=http://localhost:11434
MEMORY_TOKEN_LIMIT=1800
```

As chaves de API não são necessárias para a execução local com Ollama.

### Interface Streamlit

```bash
streamlit run streamlit_app.py
```

### Interface de terminal

```bash
python app.py --session demonstracao
```

Use a mesma sessão por pelo menos três turnos para demonstrar a memória.

## Modelo exigido e ambiente de desenvolvimento

O núcleo usa `ChatOllama` e aceita `gpt-oss:120b`, conforme o enunciado. Esse
modelo não cabe na máquina de desenvolvimento de 16 GB. Por isso, os testes locais
reproduzíveis foram executados com `qwen3:4b-instruct`. Para testar o modelo de 120B,
configure `OLLAMA_MODEL=gpt-oss:120b` e aponte `OLLAMA_BASE_URL` para um servidor
Ollama compatível.

## Avaliações

Execute os mesmos casos com o modelo usado nas métricas do relatório:

```bash
python -m evals.run_evals --variant legacy --model qwen3:4b-instruct
python -m evals.run_evals --variant sprint3 --model qwen3:4b-instruct
python -m evals.run_structured_evals --model qwen3:4b-instruct
```

Evidências versionadas:

- `evals/legacy_results.json`: 7/11 casos aprovados (63,64%).
- `evals/sprint3_results.json`: 11/11 casos aprovados (100%).
- `evals/structured_results.json`: 3/3 extrações válidas (100%).

## Publicação no Streamlit Community Cloud

A demonstração pública usa OpenRouter com um modelo Nemotron conversacional. Em
**Advanced settings > Secrets**, configure:

```toml
LLM_PROVIDER = "openrouter"
OPENROUTER_API_KEY = "sua-chave-openrouter"
OPENROUTER_MODEL = "nvidia/nemotron-3.5-lightning:free"
```

Também é possível usar diretamente a NVIDIA API:

```toml
LLM_PROVIDER = "nvidia"
NVIDIA_API_KEY = "sua-chave-nvapi"
NVIDIA_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"
```

Nunca salve chaves reais no GitHub. O projeto carrega as credenciais apenas por
variáveis de ambiente, `.env` ignorado pelo Git ou Secrets da hospedagem.

## Estrutura principal

```text
prompts/       versões do system prompt
src/chain/     construção LCEL e memória
src/schemas/   schema Pydantic v2
src/guardrails validação de segurança e escopo
evals/         casos, executores e resultados
docs/          baseline, relatório de modelos e PDF final
```

O código das Sprints 1 e 2 usado como baseline está documentado em
[`docs/baseline_sprints_1_2.md`](docs/baseline_sprints_1_2.md).
