# Instância de referência: Interpretador MiniPar

| Item | Caminho |
|------|---------|
| Hotspot | `packages/minipar-core/minipar_core/translation/interpreter.py` |
| Classe | `InterpreterBackend` |
| Algoritmo | Execução direta da AST (sem TAC) |
| Microsserviço | `microservices/ms-interpreter/` |
| Registry | `INTERPRETER` em `backend-registry.ts` |
| Variante LPS | Interpretador + LOCAL ou DISTRIBUTED_SOCKETS |

**Frozen-spots reutilizados:** lexer, parser, semântica, gateway, frontend.
