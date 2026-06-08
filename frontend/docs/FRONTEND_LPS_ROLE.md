# Papel do Frontend no MiniPar Framework (casca LPS)

O Angular em `frontend/` é a **instância de referência da UI LPS** — frozen-spot de infraestrutura, **não** hotspot de algoritmo de compilação.

## O que o frontend faz

| Componente | Papel | Tipo |
|------------|-------|------|
| `code-editor.component` | Editor de código MiniPar | Infraestrutura reutilizável |
| `feature-panel.component` | Seleção de variabilidade LPS | Configuração de produto (binding runtime) |
| `compiler-workspace` | Disparo `POST /api/v1/process` | Cliente do contrato do framework |
| `output-panel` | Exibição de saída, AST, símbolos | Infraestrutura reutilizável |

## O que o frontend NÃO faz

- Não implementa `emit()` nem `finalize()`
- Não gera código C, Rust, Python, etc.
- Não executa lexer, parser ou semântica

O hotspot de tradução fica nos microsserviços de back-end (`ms-interpreter`, `ms-codegen-*`).

## Fluxo

```
UI (feature-panel) → targetVariability = "PYTHON" | "C" | ...
  → POST /api/v1/process
  → Gateway (pipeline frozen-spot)
  → MS backend (hotspot emit/finalize)
  → Resposta → output-panel
```

## Alterações ao estender novo back-end

Configuração LPS (não algoritmo) — 3 arquivos:

| Arquivo | Alteração |
|---------|-----------|
| `feature-panel.component.ts` | `{ value: 'PYTHON', label: '...' }` no array `targets` |
| `process.models.ts` | `'PYTHON'` no type `TargetVariability` |
| `api-gateway/.../target-variability.enum.ts` | `PYTHON = 'PYTHON'` |

## Evolução: variantes dinâmicas

O gateway expõe `GET /api/v1/variants` lendo `BACKEND_REGISTRY`. O frontend pode carregar opções dinamicamente (OCP completo na UI) em vez de hardcode — evolução documentada, não obrigatória para MVP.

## Substituição do frontend

Qualquer cliente HTTP que respeite o contrato reusa o framework:

```json
POST /api/v1/process
{ "sourceCode": "...", "targetVariability": "PYTHON", "executionMode": "LOCAL" }
```

Alternativas: CLI curl, extensão VS Code, script Python, outro front-end React.
