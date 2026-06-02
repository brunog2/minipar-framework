# Diagramas — MiniPar Framework

Diagramas em [Mermaid](https://mermaid.js.org/) (`.mmd`) da arquitetura do sistema.

| Arquivo | Conteúdo |
|---------|----------|
| [architecture.mmd](./architecture.mmd) | Componentes, LPS, `minipar-core`, MS Fases 1–2 |
| [pipeline-sequence.mmd](./pipeline-sequence.mmd) | Sequência `POST /api/v1/process` com back-ends reais |
| [frontend-semantic-flow.mmd](./frontend-semantic-flow.mmd) | Fluxo léxico → sintático → semântico (Fase 1) |
| [template-method.mmd](./template-method.mmd) | Template Method — classDiagram (Fase 2) |
| [codegen-c-flow.mmd](./codegen-c-flow.mmd) | Fluxo AST → TAC → C → gcc (Fase 2) |
| [reuse-map.mmd](./reuse-map.mmd) | Mapa reuso `code_references` → `minipar-core` |
| [validation-cases.mmd](./validation-cases.mmd) | Casos de teste manual Fases 1 e 2 |
| [feature-tree.mmd](./feature-tree.mmd) | Árvore de features LPS |
| [sequence-3-machines.mmd](./sequence-3-machines.mmd) | Sequência teste 3 máquinas (Fase 3) |
| [uml-use-cases.mmd](./uml-use-cases.mmd) | Casos de uso |
| [uml-components.mmd](./uml-components.mmd) | Componentes UML |
| [uml-classes-framework.mmd](./uml-classes-framework.mmd) | Classes do framework |

**Conformidade vs. requisitos:** [../../COMPLIANCE_AUDIT.md](../../COMPLIANCE_AUDIT.md)

## Status (jun/2026)

| Componente | Status |
|------------|--------|
| `ms-front-end` (:3001) | Implementado |
| `ms-semantic` (:3002) | Implementado |
| `ms-interpreter` (:3003) | Implementado |
| `ms-codegen-c` (:3004) | Implementado (gcc -O2) |
| `ms-codegen-rust` (:3005) | MVP |
| `ms-codegen-arm` (:3007) | MVP |
| `packages/minipar-core/translation` | Template Method + TAC + interpreter |
| `ms-parallel-coord` (:3006) | 🟡 implementado; gaps em [COMPLIANCE_AUDIT.md](../../COMPLIANCE_AUDIT.md) |
| `worker-quicksort` / `matrix` / `factorial` (:9001–9003) | Implementado (socket) |
| `PIPELINE_MODE` | `http` |
| `PIPELINE_BACKEND_MODE` | `http` no Docker Compose |

## Como visualizar

1. **VS Code / Cursor** — extensão Mermaid ou preview do `.mmd`.
2. **[Mermaid Live Editor](https://mermaid.live/)** — colar o conteúdo.
3. **Relatório (Overleaf / PDF)** — exportar SVG/PNG (`mmdc` ou Live Editor).

## Legenda rápida

- **Análise:** `ms-front-end` → `ms-semantic` em toda compilação.
- **LPS:** um back-end por requisição; MS reais desde Fase 2.
- **Deploy:** frontend em [https://minipar-framework.vercel.app/](https://minipar-framework.vercel.app/); stack completa via `docker compose up --build`.
