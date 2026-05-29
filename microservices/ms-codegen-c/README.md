# ms-codegen-c

## Responsabilidade

Converter AST JSON validada em **código C** (ou **C++** quando `target: CPP`) compilável. Invocar `gcc -O2` (ou `g++`) para gerar executável de alta performance.

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| `POST` | `/generate` | Gera código e opcionalmente compila |
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

`target` pode ser `C` ou `CPP` (variante LPS; mesmo MS, hotspot Template Method).

## Contrato de saída

```json
{
  "output": "Compilação concluída",
  "code": "/* C gerado */",
  "executablePath": "/tmp/out.exe"
}
```

## Reuso de software

| Componente | Referência |
|------------|------------|
| Gerador C | `code_references/projeto_compiladores/src/c_codegen.py` |
| Compilação gcc -O2 | `code_references/projeto_compiladores/src/backend.py` |

## Variabilidade LPS

| Ponto de variação | Variante |
|-------------------|----------|
| Back-end | **C**, **CPP** |

## Status

**Não implementado** nesta fase de setup.
