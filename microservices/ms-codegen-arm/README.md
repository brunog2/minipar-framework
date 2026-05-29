# ms-codegen-arm

## Responsabilidade

Gerar **Assembly ARMv7** a partir da AST/TAC para execução em ambiente ARM (ex.: Raspberry Pi, QEMU).

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| `POST` | `/generate` | Gera `.s` ARMv7 |
| `GET` | `/health` | Health check |

## Contrato de entrada

```json
{
  "ast": { "type": "Program", "declarations": [] },
  "symbolTable": {},
  "executionMode": "LOCAL",
  "target": "ASSEMBLY"
}
```

## Contrato de saída

```json
{
  "output": "Assembly gerado",
  "code": ".text\n.global _start\n..."
}
```

## Reuso de software

| Componente | Referência |
|------------|------------|
| ARM codegen | `code_references/projeto_compiladores/src/arm_codegen.py` |
| Guia ARM | `code_references/projeto_compiladores/docs/tutorials/ARM_COMPILATION_GUIDE.md` |

## Variabilidade LPS

| Ponto de variação | Variante |
|-------------------|----------|
| Back-end | **ASSEMBLY** (ARMv7) |

## Status

**Não implementado** nesta fase de setup.
