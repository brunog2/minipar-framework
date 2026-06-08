# Instâncias de referência — MiniPar Framework

Estas pastas catalogam **aplicações (instâncias LPS)** criadas **sobre** o framework MiniPar 2026.1. Cada instância reutiliza os frozen-spots (lexer, parser, semântica, gateway, pipeline) e preenche os hotspots de tradução (`emit()`, `finalize()`).

> **Não é um gerador de projetos.** O código do framework permanece no monorepo; o desenvolvedor implementa hotspots e registra a variante — ver [CREATING_AN_APPLICATION.md](../CREATING_AN_APPLICATION.md).

## Mapa framework vs instância

| Camada | Tipo | Artefatos |
|--------|------|-----------|
| Framework (frozen-spot) | Invariante | `minipar-core`, `api-gateway`, `ms-front-end`, `ms-semantic`, `frontend/` |
| Contrato | Assinatura fixa | `AbstractBackendTranslator`, `BACKEND_REGISTRY`, `_AST_CONTRACT.md` |
| Instância (hotspot) | Código do dev | `*_backend.py`, microsserviço `ms-*`, 1 linha no registry |

## Catálogo de instâncias

| Instância | Pasta | Hotspot | Microsserviço |
|-----------|-------|---------|---------------|
| Interpretador MiniPar | [reference-interpreter/](reference-interpreter/) | `InterpreterBackend.emit()` | `ms-interpreter` |
| Compilador → C | [reference-compiler-c/](reference-compiler-c/) | `CBackend.emit()` | `ms-codegen-c` |
| Compilador → C++ | [reference-compiler-cpp/](reference-compiler-cpp/) | `CppBackend.emit()` | `ms-codegen-c` |
| Compilador → Rust | [reference-compiler-rust/](reference-compiler-rust/) | `RustBackend.emit()` | `ms-codegen-rust` |
| Compilador → ARM | [reference-compiler-arm/](reference-compiler-arm/) | `ARMBackend.emit()` | `ms-codegen-arm` |
| **Extensão Python (demo)** | [extension-python/](extension-python/) | `PythonBackend.emit()` | `ms-codegen-python` |

## Extensão vs referência

As instâncias `reference-*` foram implementadas pela equipe como variantes LPS de produção. A pasta `extension-python/` documenta uma **extensão nova** adicionada para demonstrar o processo de instanciação na banca (simula um dev externo preenchendo hotspots).

## Como criar nova instância

1. Copie `packages/minipar-core/minipar_core/translation/_template_backend.py`
2. Implemente `emit()` e `finalize()`
3. Crie microsserviço FastAPI (`POST /generate` ou `/execute`)
4. Adicione entrada em `api-gateway/src/pipeline/backend-registry.ts`
5. Exponha variante na UI (`feature-panel.component.ts`) — configuração LPS, não algoritmo

Guia completo: [CREATING_AN_APPLICATION.md](../CREATING_AN_APPLICATION.md)
