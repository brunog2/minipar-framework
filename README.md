# MiniPar Framework 2026.1

Framework para compiladores e interpretadores da linguagem **MiniPar 2026.1** (OO + paralelismo real), organizado como **Linha de Produto de Software (LPS)** com arquitetura de **microsserviços**.

## Como estender o framework

- **[CREATING_AN_APPLICATION.md](CREATING_AN_APPLICATION.md)** — passo a passo para criar nova instância (framework vs gerador, FAQ banca)
- **[applications/](applications/)** — catálogo de instâncias de referência + extensão Python
- **[packages/minipar-core/EXTENDING.md](packages/minipar-core/EXTENDING.md)** — contrato de hotspots (`emit`/`finalize`)
- **[packages/minipar-core/minipar_core/translation/_template_backend.py](packages/minipar-core/minipar_core/translation/_template_backend.py)** — esqueleto vazio para copiar

## Pontos de variação (LPS)

| Ponto de variação | Variantes |
|-------------------|-----------|
| Modo de execução | Interpretador, Compilador |
| Back-end de compilação | C, C++, Rust, Assembly ARMv7, **Python (extensão demo)** |
| Ambiente de execução | Local, Distribuído (sockets, 3 máquinas) |

## Pipeline de dados

```
Código MiniPar (Frontend)
  → API Gateway (POST /api/v1/process)
  → ms-front-end (Lexer/Parser → AST JSON)
  → ms-semantic (Tabela de símbolos)
  → Backend escolhido (Interpreter / Codegen / Parallel coord)
  → Resposta + log em PostgreSQL
```

## Diagramas de arquitetura

Diagramas Mermaid em [`docs/diagrams/`](docs/diagrams/):

- [architecture.mmd](docs/diagrams/architecture.mmd) — componentes, LPS, deploy e reuso
- [pipeline-sequence.mmd](docs/diagrams/pipeline-sequence.mmd) — sequência `POST /api/v1/process`
- [validation-cases.mmd](docs/diagrams/validation-cases.mmd) — casos de validação manual (Fase 1)
- [template-method.mmd](docs/diagrams/template-method.mmd) — Template Method (Fase 2)
- [codegen-c-flow.mmd](docs/diagrams/codegen-c-flow.mmd) — AST → C → gcc (Fase 2)
- [reuse-map.mmd](docs/diagrams/reuse-map.mmd) — mapa de reuso (Fase 2)

## Estrutura do monorepo

```
minipar-framework/
├── applications/             # Instâncias de referência + extensão Python
├── CREATING_AN_APPLICATION.md
├── frontend/                 # Angular + nginx (:4200)
├── api-gateway/              # NestJS — orquestração (:3000)
├── packages/minipar-core/    # Lexer, parser, semântica, translation/
├── microservices/
│   ├── ms-front-end/         # :3001 — parse
│   ├── ms-semantic/          # :3002 — analyze
│   ├── ms-interpreter/       # :3003 — execute
│   ├── ms-codegen-c/         # :3004 — generate (gcc -O2)
│   ├── ms-codegen-rust/      # :3005 — generate (MVP)
│   ├── ms-codegen-arm/       # :3007 — generate (MVP)
│   └── ms-codegen-python/    # :3008 — generate (extensão demo)
├── database/init.sql
├── docs/diagrams/            # Diagramas Mermaid
├── sources/examples/         # Fixtures 01–16
├── COMPLIANCE_AUDIT.md       # Conformidade vs. requisitos + backlog futuro
└── docker-compose.yml
```

## Requisitos

- Node.js 20+ (frontend / api-gateway local)
- Docker e Docker Compose (stack completa)
- GCC incluído no container `ms-codegen-c` (não precisa instalar no host para E2E Docker)

## Execução com Docker

```bash
cd minipar-framework
docker compose up --build
```

Serviços (Docker Compose):

| Serviço | Porta host |
|---------|------------|
| frontend | 4200 |
| api-gateway | 3000 |
| ms-front-end | 3001 |
| ms-semantic | 3002 |
| ms-interpreter | 3003 |
| ms-codegen-c | 3004 |
| ms-codegen-rust | 3005 |
| ms-codegen-arm | 3007 |
| ms-codegen-python | 3008 |
| postgres | rede interna |

Variáveis no gateway: `PIPELINE_MODE=http`, `PIPELINE_BACKEND_MODE=http`.

## Deploy

### Frontend (Vercel)

Interface web em produção: **[https://minipar-framework.vercel.app/](https://minipar-framework.vercel.app/)**

| Ambiente | URL |
|----------|-----|
| Produção (Vercel) | https://minipar-framework.vercel.app/ |
| Docker / local | http://localhost:4200 |

## Desenvolvimento local

### API Gateway

```bash
cd api-gateway
cp .env.example .env
npm run start:dev
```

### Frontend

```bash
cd frontend
npm start
```

Configure `src/environments/environment.ts` se o gateway não estiver em `http://localhost:3000`.

## Modo pipeline

| Variável | Comportamento |
|----------|---------------|
| `PIPELINE_MODE` | `mock` — respostas simuladas; `http` — chama MS reais (padrão no Docker Compose) |
| `PIPELINE_BACKEND_MODE` | `mock` — interpretador/codegen simulados; `http` — MS reais (padrão Docker Compose Fase 2) |

### Fase 1 (implementado)

| Serviço | Porta | Status |
|---------|-------|--------|
| ms-front-end | 3001 | ✅ POST /parse |
| ms-semantic | 3002 | ✅ POST /analyze |

### Fase 2 (implementado)

| Serviço | Porta | Status |
|---------|-------|--------|
| ms-interpreter | 3003 | ✅ POST /execute |
| ms-codegen-c | 3004 | ✅ POST /generate (gcc -O2) |
| ms-codegen-rust | 3005 | ✅ POST /generate (MVP) |
| ms-codegen-arm | 3007 | ✅ POST /generate (MVP) |
| ms-parallel-coord | 3006 | 🟡 POST /coordinate (workers socket; ver COMPLIANCE_AUDIT.md) |

Pacote compartilhado: [`packages/minipar-core/`](packages/minipar-core/) — inclui `translation/` (Template Method).

Exemplos: [`sources/examples/`](sources/examples/) (01–14).

**Gestão do projeto:** [COMPLIANCE_AUDIT.md](./COMPLIANCE_AUDIT.md) · [SCHEDULE.md](./SCHEDULE.md) · [ACTIVITIES.md](./ACTIVITIES.md) · [ROADMAP.md](./ROADMAP.md).

## Referências de reuso

Código base em `../code_references/`:

- **OO / AST:** `cl-minipar` (Java)
- **Codegen C/ARM:** `projeto_compiladores` (Python)

## Verificação E2E

```bash
curl http://localhost:3000/health

curl -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"sourceCode":"class Main { void run() { println(\"ok\"); } }","targetVariability":"INTERPRETER","executionMode":"LOCAL"}'
```

Interface em http://localhost:4200 — botão **Executar** (ou `Ctrl+Enter` / `F5`), painel **Console** com abas Saída / Símbolos / AST. Exemplos e erros esperados: [`sources/examples/README.md`](sources/examples/README.md).

Histórico no Postgres:

```bash
docker exec minipar-postgres psql -U minipar -d minipar \
  -c "SELECT id, status, target_variability FROM compilation_history ORDER BY created_at DESC LIMIT 5;"
```

## Roadmap completo

| Documento | Conteúdo |
|-----------|----------|
| [ROADMAP.md](./ROADMAP.md) | Entregas técnicas por fase |
| [SCHEDULE.md](./SCHEDULE.md) | Cronograma e datas |
| [ACTIVITIES.md](./ACTIVITIES.md) | Sprints, donos, checklist E2E |
| [COMPLIANCE_AUDIT.md](./COMPLIANCE_AUDIT.md) | O que está conforme / parcial / não conforme |

## Roadmap (resumo)

1. ~~Implementar `ms-front-end` e `ms-semantic`~~ (Fase 1)
2. ~~Template Method + `ms-interpreter`, `ms-codegen-c`, Rust/ARM MVP~~ (Fase 2)
3. ~~`ms-parallel-coord` + workers socket~~ (Fase 3 — 🟡 validar E2E; ver auditoria)
4. ~~Fractal Sierpinski (`13_sierpinski.minipar`)~~ (Fase 3 — 🟡 validar na UI + PDF)

## Entrega acadêmica

Ver [PROJECT_REQUIREMENTS.md](../PROJECT_REQUIREMENTS.md) — entrega **10 de junho**.
