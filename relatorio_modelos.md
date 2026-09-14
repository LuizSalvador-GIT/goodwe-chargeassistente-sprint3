# Relatório de modelos e parâmetros

## Parâmetros comuns

- temperature: 0,2
- top_p: 0,9
- max_tokens / num_predict: 512
- memória: 1.800 tokens

## Modelos comparados

### Llama 3 8B - baseline histórica

Modelo usado nas Sprints 1/2 com temperature 0,3, top_p 0,9 e num_predict 512. O relatório anterior classificou 11/11 respostas como adequadas, mas não guardou latência, tokens nem saída estruturada. A baseline reconstruída no eval atual preserva o prompt e o fluxo manual, usando o mesmo Qwen da Sprint 03 para isolar o efeito da refatoração.

### qwen3:4b-instruct - execução local reproduzível

No eval atual, obteve 11/11 casos na versão LCEL, latência média de 19,54 s, 13,27 tokens médios de entrada e 161,55 de saída. No fluxo legado reconstruído, obteve 7/11, latência de 22,38 s e 118,09 tokens de saída. O structured output acertou 3/3 casos.

### gpt-oss:120b - modelo principal configurado

É o padrão do projeto e será acessado por `ChatOllama`. Seu arquivo local tem aproximadamente 65 GB, acima da capacidade disponível no Mac de 16 GB; por isso não foram inventadas métricas. Para a validação final, configure um `OLLAMA_BASE_URL` remoto ou use um ambiente compatível e reexecute os mesmos comandos.

## Conclusão

O Qwen permitiu validar toda a arquitetura e medir a evolução. O Llama 3 documenta a baseline histórica e o gpt-oss:120b permanece como alvo exigido. A troca de modelo não altera prompt, memória, parser, schema ou eval.
