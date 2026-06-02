# ms-parallel-coord

## Responsabilidade

Coordenar execução **distribuída** quando `executionMode: DISTRIBUTED_SOCKETS`:

- Menu central dispara tarefas em até **3 máquinas**
- QuickSort (máquina 1), multiplicação de matrizes (máquina 2), fatorial (máquina 3)
- Resultados retornam via **sockets**

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| `POST` | `/coordinate` | Orquestra jobs distribuídos |
| `GET` | `/health` | Health check |

## Contrato de entrada

```json
{
  "ast": { "type": "Program", "declarations": [] },
  "symbolTable": {},
  "executionMode": "DISTRIBUTED_SOCKETS",
  "hosts": [
    { "role": "quicksort", "host": "192.168.1.10", "port": 9001 },
    { "role": "matrix", "host": "192.168.1.11", "port": 9002 },
    { "role": "factorial", "host": "192.168.1.12", "port": 9003 }
  ]
}
```

## Contrato de saída

```json
{
  "output": "Resultados agregados do menu coordenador",
  "results": [
    { "role": "quicksort", "data": "..." },
    { "role": "matrix", "data": "..." },
    { "role": "factorial", "data": "..." }
  ]
}
```

## Reuso de software

| Componente | Referência |
|------------|------------|
| Exemplos socket MiniPar | `code_references/projeto_compiladores/examples/quicksort.minipar`, `calc_server.minipar`, `test_echo_*.minipar` |
| Canal TCP Java | `code_references/cl-minipar/src/io/TCPChannel.java` |
| Tutorial canais | `code_references/projeto_compiladores/docs/tutorials/CHANNEL_TUTORIAL.md` |

## Variabilidade LPS

| Ponto de variação | Variante |
|-------------------|----------|
| Ambiente | **LOCAL** vs **DISTRIBUTED_SOCKETS** |

## Ordem no pipeline (gateway)

Quando `DISTRIBUTED_SOCKETS`, o gateway chama este MS **após** semântica e **antes** do back-end escolhido (documentado no `PipelineService`).

## Status

**Implementado** — Fase 3. Coordenador FastAPI + 3 workers socket (`worker-quicksort`, `worker-matrix`, `worker-factorial`) no Docker Compose.
