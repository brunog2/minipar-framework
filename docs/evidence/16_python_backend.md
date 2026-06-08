# Evidência E2E — Backend Python (extensão demo)

## Fixture

- Arquivo: `sources/examples/16_codegen_python.minipar`
- Variante LPS: `PYTHON`
- Modo: `LOCAL`

## Comportamento esperado

1. Pipeline: `ms-front-end: parse` → `ms-semantic: analyze` → `ms-codegen-python: generate`
2. `success: true`
3. `targetVariability`: `PYTHON`
4. Saída contém `Executado com python3` e a linha `hello from Python backend`
5. `generatedCode` contém docstring `Gerado pelo MiniPar PythonBackend`
6. Código gerado inclui `def Main_run():` e `print('hello from Python backend')`

## Teste manual (curl)

```bash
curl -s -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{
    "sourceCode": "class Main { void run() { println(\"hello from Python backend\"); } }",
    "targetVariability": "PYTHON",
    "executionMode": "LOCAL"
  }'
```

## Teste na UI

1. Abrir http://localhost:4200
2. Selecionar **Compilador → Python (extensão)**
3. Colar o conteúdo de `16_codegen_python.minipar`
4. Executar — console deve exibir stdout do `python3`

## Saída esperada (output)

```
Executado com python3
hello from Python backend
```

## Código gerado esperado (trecho)

```python
"""Gerado pelo MiniPar PythonBackend (extensão demo)."""

def Main_run():
    print("hello from Python backend")

if __name__ == "__main__":
    Main_run()
```

## O que esta demo prova (banca)

- Extensão **sem alterar** `AbstractBackendTranslator.translate()` (frozen-spot)
- Novo hotspot `PythonBackend.emit()` + microsserviço + 1 linha no registry
- Mesmo pipeline léxico-sintático-semântico das outras instâncias
