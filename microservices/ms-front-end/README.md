# ms-front-end

## Responsabilidade

Análise **léxica** e **sintática** do código MiniPar 2026.1. Produz a **AST em JSON** para o restante do pipeline.

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| `POST` | `/parse` | Recebe código-fonte; retorna AST |
| `GET` | `/health` | Health check |

## Contrato de entrada

```json
{
  "sourceCode": "class A { ... }"
}
```

## Contrato de saída

```json
{
  "ast": { "type": "Program", "declarations": [] },
  "errors": []
}
```

Ver também: [_AST_CONTRACT.md](../_AST_CONTRACT.md).

## Reuso de software

| Componente | Referência |
|------------|------------|
| Lexer | `code_references/cl-minipar/src/lexer/Lexer.java` |
| Parser | `code_references/cl-minipar/src/parser/Parser.java` |
| AST | `code_references/cl-minipar/src/parser/ast/*.java` |

## Variabilidade LPS

- **Ponto de variação:** fase de análise front-end  
- **Variante:** única (parser OO 2026.1)

## Status

**Não implementado** nesta fase de setup — especificação apenas.
