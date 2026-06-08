# Instância de referência: Compilador MiniPar → C

| Item | Caminho |
|------|---------|
| Hotspot | `packages/minipar-core/minipar_core/translation/c_backend.py` |
| Classe | `CBackend` |
| Algoritmo | TAC → C → `gcc -O2` |
| Microsserviço | `microservices/ms-codegen-c/` |
| Registry | `C` em `backend-registry.ts` |
| Exemplo | `sources/examples/11_codegen_c.minipar` |

**Frozen-spots reutilizados:** lexer, parser, semântica, TACGenerator, gateway, frontend.
