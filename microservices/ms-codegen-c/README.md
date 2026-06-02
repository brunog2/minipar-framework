# ms-codegen-c

## Responsabilidade

Converter AST JSON validada em **código C** (ou **C++** quando `target: CPP`) compilável. Invocar `gcc -O2` (ou `g++`) para gerar executável de alta performance.

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| `POST` | `/generate` | Gera código e compila |
| `GET` | `/health` | Health check |

## Contrato de entrada

```json
{
  "ast": { "type": "Program", "declarations": [] },
  "symbolTable": {},
  "executionMode": "LOCAL",
  "target": "C"
}
```

`target` pode ser `C` ou `CPP` (variante LPS; hotspot Template Method).

## Contrato de saída

```json
{
  "output": "Compiled with gcc -O2\nok\n",
  "code": "/* C gerado */"
}
```

## Reuso de software

| Componente | Referência |
|------------|------------|
| TAC + Gerador C | `code_references/projeto_compiladores/src/codegen.py`, `c_codegen.py` |
| Compilação gcc -O2 | `code_references/projeto_compiladores/src/backend.py` |
| Implementação | `packages/minipar-core/minipar_core/translation/c_backend.py` |

## Variabilidade LPS

| Ponto de variação | Variante |
|-------------------|----------|
| Back-end | **C**, **CPP** |

## Status

**Implementado** (Fase 2 — jun/2026). Docker inclui `gcc`/`g++`, porta **3004**.
