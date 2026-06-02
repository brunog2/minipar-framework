# Contrato AST JSON (MiniPar 2026.1)

Representação JSON alinhada aos nós Java em `code_references/cl-minipar/src/parser/ast/`.

## Exemplo mínimo

```json
{
  "type": "Program",
  "declarations": [
    {
      "type": "ClassDecl",
      "name": "Foo",
      "extends": null,
      "members": []
    }
  ]
}
```

## Nós principais

| Tipo | Descrição |
|------|-----------|
| `Program` | Raiz; `declarations[]` |
| `ClassDecl` | OO: `name`, `extends`, `members[]` |
| `MethodDecl` | `name`, `parameters[]`, `returnType`, `body` |
| `FuncDecl` | Função global |
| `ParBlock` / `SeqBlock` | Paralelismo e sequência |
| `SendStmt` / `ReceiveStmt` | Comunicação via canal |
| `NewInstance` | `new T()` |
| `MethodCall` | Chamada de método |

**Status nesta fase:** implementado em `packages/minipar-core` (`ast_json.to_dict`).
