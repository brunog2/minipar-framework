# Extensão nova (demo banca): Compilador MiniPar → Python

Esta pasta documenta a **única extensão claramente separada** do conjunto de instâncias de referência — simula um desenvolvedor externo preenchendo hotspots sem alterar o framework.

## Artefatos da extensão

| Passo | Artefato | Caminho |
|-------|----------|---------|
| 1 | Hotspot `emit()` / `finalize()` | `packages/minipar-core/minipar_core/translation/python_backend.py` |
| 2 | Função de entrada | `generate_python()` em `translation/__init__.py` |
| 3 | Microsserviço thin wrapper | `microservices/ms-codegen-python/` |
| 4 | Registry (1 linha) | `PYTHON` em `backend-registry.ts` |
| 5 | UI (1 linha) | `PYTHON` em `feature-panel.component.ts` |
| 6 | Docker Compose | `ms-codegen-python:3008` |
| 7 | Exemplo | `sources/examples/16_codegen_python.minipar` |
| 8 | Evidência E2E | `docs/evidence/16_codegen_python_output.txt` |

## Diff mínimo vs framework existente

```
+ python_backend.py          (hotspot — código do dev)
+ ms-codegen-python/         (wiring da instância)
+ backend-registry.ts        (+1 entrada PYTHON)
+ feature-panel + enums      (+1 variante LPS)
+ docker-compose.yml         (+1 serviço)
```

**Não alterado:** `AbstractBackendTranslator.translate()`, pipeline do gateway, lexer, parser, semântica.

## Demonstração na banca

1. Mostrar `reference-compiler-c` (instância existente)
2. Mostrar `extension-python` (extensão nova)
3. Executar exemplo 16 com variante **PYTHON** na UI
4. Exibir código Python gerado + stdout
