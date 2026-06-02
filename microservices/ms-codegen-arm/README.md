# ms-codegen-arm

## Responsabilidade

Gerar **Assembly ARMv7** a partir da AST/TAC.

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| `POST` | `/generate` | Gera `.s` ARMv7 |
| `GET` | `/health` | Health check |

## Contrato de saída

```json
{
  "output": "Assembly ARMv7 gerado. ...",
  "code": ".text\n.global main\n..."
}
```

## Reuso de software

| Componente | Referência |
|------------|------------|
| ARM codegen | `code_references/projeto_compiladores/src/arm_codegen.py` |
| Implementação MVP | `packages/minipar-core/minipar_core/translation/arm_backend.py` |

## Status

**Implementado MVP** (Fase 2 — jun/2026). Porta **3007**. Execução ARM opcional (toolchain pode estar ausente).
