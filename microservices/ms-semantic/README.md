# ms-semantic

## Responsabilidade

**Análise semântica**: verificação de tipos, escopos, herança OO e construção da **tabela de símbolos**. Recebe AST JSON validada sintaticamente.

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| `POST` | `/analyze` | Analisa AST; retorna AST anotada + symbolTable |
| `GET` | `/health` | Health check |

## Contrato de entrada

```json
{
  "ast": { "type": "Program", "declarations": [] }
}
```

## Contrato de saída

```json
{
  "ast": { "type": "Program", "declarations": [] },
  "symbolTable": {
    "scopes": [{ "name": "global", "symbols": [] }]
  },
  "errors": []
}
```

## Reuso de software

| Componente | Referência |
|------------|------------|
| Analisador semântico | `code_references/projeto_compiladores/src/semantic.py` |
| Tabela de símbolos | `code_references/projeto_compiladores/src/symbol_table.py` |

**Nota:** estender para classes, `extends`, `new` conforme AST Java do `cl-minipar`.

## Variabilidade LPS

- **Ponto de variação:** análise estática  
- **Variante:** regras OO 2026.1 (obrigatório para todos os back-ends)

## Status

**Implementado** (Fase 1 — jun/2026). Análise sobre AST JSON via `minipar_core.semantic_json`.

### Erros semânticos (exemplo)

| Entrada | Mensagem |
|---------|----------|
| `class Dog extends Arvore` (Arvore inexistente) | `Semantic error: Superclass 'Arvore' not found for class 'Dog'` |

Fixture: `sources/examples/04_semantic_extends_unknown.minipar`.
