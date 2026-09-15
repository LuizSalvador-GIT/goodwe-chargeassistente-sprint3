# Relatório de modelos e parâmetros

## Parâmetros comuns

- temperature: 0,2
- top_p: 0,9
- max_tokens / num_predict: 512
- memória: 1.800 tokens

## Modelos comparados

### Llama 3 8B - baseline histórica

Modelo usado nas Sprints 1/2 com temperature 0,3, top_p 0,9 e num_predict 512. O relatório anterior classificou 11/11 respostas como adequadas, mas não guardou latência, tokens nem saída estruturada. A baseline reconstruída no eval atual preserva o prompt e o fluxo manual, usando o mesmo Qwen da Sprint 03 para isolar o efeito da refatoração.

### qwen3:4b-instruct - execução local

Na comparação entre modelos de 15/09/2026, obteve 10/11 casos (90,91%), latência média de 21,17 s, 13,27 tokens médios de entrada e 161,55 de saída. O caso `support_01` falhou por recomendar lavar um conector, orientação proibida pelo eval. Na execução anterior do comparativo de arquitetura, obteve 11/11 na versão LCEL e 7/11 no fluxo legado reconstruído. O structured output acertou 3/3 casos.

### NVIDIA Nemotron 3.5 Lightning 30B A3B - API NVIDIA

Executado em 15/09/2026 com o mesmo prompt v3, os mesmos 11 casos e parâmetros equivalentes. Obteve 11/11 casos (100%), latência média de 12,31 s, 13,27 tokens médios de entrada e 136,45 de saída. Em relação ao Qwen nessa rodada, ganhou 9,09 pontos percentuais de qualidade, reduziu a latência média em 41,88% e produziu respostas 15,54% menores.

### gpt-oss:120b - modelo principal configurado

É o padrão do projeto e será acessado por `ChatOllama`. Seu arquivo local tem aproximadamente 65 GB, acima da capacidade disponível no Mac de 16 GB; por isso não foram inventadas métricas. Para a validação final, configure um `OLLAMA_BASE_URL` remoto ou use um ambiente compatível e reexecute os mesmos comandos.

## Conclusão

O Nemotron apresentou o melhor resultado na comparação medida, com 100% de aprovação e menor latência. O Qwen continua útil para execução local sem custo de API. O Llama 3 documenta a baseline histórica e o gpt-oss:120b permanece como alvo exigido. A troca de modelo não altera prompt, memória, parser, schema ou eval.
