# Baseline das Sprints 1 e 2

Fonte: <https://github.com/VictorManzini/sprint1/tree/main/prompt_ia>

- Produto: ChargeAssistente — GoodWe ChargeGrid / EV ChargeOps.
- Persona: morador de condomínio com eletropostos compartilhados.
- Stack: Streamlit, SDK Python do Ollama e Llama 3 8B.
- Memória: lista manual no `st.session_state`, limitada às últimas 20 mensagens.
- Prompt: versão 2, com escopo, escalada humana, segurança e exemplos few-shot.
- Eval: 11 casos qualitativos; resultado documentado como 11/11 adequados.
- Parâmetros: temperature 0.3, top_p 0.9 e num_predict 512.

Não foram registrados tokens por turno, latência média ou acurácia de structured output.
Essas métricas serão produzidas ao reexecutar a baseline e a versão LCEL nas mesmas
condições. O histórico original permanece no repositório de origem.
