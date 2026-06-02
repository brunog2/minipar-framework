# ms-interpreter

## Responsabilidade

**Runtime** do MiniPar: execução direta da AST + tabela de símbolos (modo **Interpretador**).

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| `POST` | `/execute` | Executa programa; retorna saída (stdout) |
| `GET` | `/health` | Health check |

## Contrato de entrada

```json
{
  "ast": { "type": "Program", "declarations": [] },
  "symbolTable": {},
  "executionMode": "LOCAL",
  "target": "INTERPRETER"
}
```

## Contrato de saída

```json
{
  "output": "linhas impressas pelo programa",
  "exitCode": 0
}
```

## Reuso de software

| Componente | Referência |
|------------|------------|
| Interpretador OO | `code_references/cl-minipar/src/interpreter/Interpreter.java` |
| Template Method | `packages/minipar-core/minipar_core/translation/interpreter.py` |

## Variabilidade LPS

| Ponto de variação | Variante |
|-------------------|----------|
| Modo de execução | **INTERPRETER** (este MS) vs compiladores |

## Status

**Implementado** (Fase 2 — jun/2026). FastAPI em `app/main.py`, porta **3003**.

MVP: classes OO, `println`, `new`, métodos, `seq`/`par` (threads), entrada automática `Main.run()`.
