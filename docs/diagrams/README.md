# Diagramas — MiniPar Framework

Diagramas em [Mermaid](https://mermaid.js.org/) (`.mmd`) da arquitetura proposta do sistema.

| Arquivo | Conteúdo |
|---------|----------|
| [architecture.mmd](./architecture.mmd) | Componentes: frontend, gateway, PostgreSQL, microsserviços, LPS, paralelismo e reuso |
| [pipeline-sequence.mmd](./pipeline-sequence.mmd) | Sequência de `POST /api/v1/process` (modo `http`) |

## Como visualizar

1. **VS Code / Cursor** — extensão [Mermaid](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) ou preview do arquivo `.mmd`.
2. **[Mermaid Live Editor](https://mermaid.live/)** — colar o conteúdo do `.mmd`.
3. **Relatório (Overleaf / PDF)** — exportar SVG ou PNG a partir do Live Editor ou `mmdc` (CLI `@mermaid-js/mermaid-cli`).

```bash
# opcional: exportar PNG (requer npm i -g @mermaid-js/mermaid-cli)
mmdc -i docs/diagrams/architecture.mmd -o docs/diagrams/architecture.png -b transparent
```

## Legenda rápida

- **Análise:** `ms-front-end` → `ms-semantic` em toda compilação.
- **LPS:** um back-end por requisição (`INTERPRETER`, `C`, `CPP`, `RUST`, `ASSEMBLY`).
- **Distribuído:** `ms-parallel-coord` quando `executionMode = DISTRIBUTED_SOCKETS`.
- **Deploy atual:** frontend em [https://minipar-framework.vercel.app/](https://minipar-framework.vercel.app/); stack completa via `docker compose` (gateway + Postgres + MS locais).
