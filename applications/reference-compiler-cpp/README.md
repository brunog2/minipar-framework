# Instância de referência: Compilador MiniPar → C++

| Item | Caminho |
|------|---------|
| Hotspot | `packages/minipar-core/minipar_core/translation/c_backend.py` |
| Classe | `CppBackend` (herda `CBackend`) |
| Algoritmo | TAC → C++ → `g++ -O2` |
| Microsserviço | `microservices/ms-codegen-c/` (mesmo MS, `target=CPP`) |
| Registry | `CPP` em `backend-registry.ts` |

Herança real: `CppBackend` sobrescreve apenas `compiler` e `std_flag`.
