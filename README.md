# MiniPar Framework 2026.1

Framework para compiladores e interpretadores da linguagem **MiniPar 2026.1** (OO + paralelismo real), organizado como **Linha de Produto de Software (LPS)** com arquitetura de **microsserviços**.

## Documentação principal — framework e hotspots

> **Para o professor:** como criar uma nova instância LPS e onde estão os hotspots reais implementados no projeto.

| Documento | Conteúdo |
|-----------|----------|
| **[CREATING_AN_APPLICATION.md](CREATING_AN_APPLICATION.md)** | Guia completo: frozen-spots vs hotspots, **dois exemplos reais** (`interpreter.py`, `c_backend.py`), passo a passo para nova variante |
| **[Relatório - Minipar 2026.1.pdf](<Relatório - Minipar 2026.1.pdf>)** | Relatório técnico final integrado (3 disciplinas) — **entrega em PDF** |
| [report.tex](report.tex) | Fonte LaTeX do relatório (recompilar com `./scripts/build-pdf.sh`) |
| [packages/minipar-core/EXTENDING.md](packages/minipar-core/EXTENDING.md) | Contrato técnico (`emit`/`finalize`, Template Method) |
| [packages/minipar-core/minipar_core/translation/](packages/minipar-core/minipar_core/translation/) | Código-fonte dos hotspots (backends de tradução) |
| [applications/](applications/) | Catálogo de instâncias de referência + extensão Python |

Hotspots de referência já no repositório:

- **Interpretador** — [`interpreter.py`](packages/minipar-core/minipar_core/translation/interpreter.py) (`INTERPRETER`)
- **Compilador C** — [`c_backend.py`](packages/minipar-core/minipar_core/translation/c_backend.py) (`C` / `CPP`)

Detalhes, trechos de código e exemplos MiniPar: **[CREATING_AN_APPLICATION.md §3](CREATING_AN_APPLICATION.md#3-exemplos-reais-de-hotspots-criados-do-zero)**.

## Equipe

| Integrante | Disciplinas |
|------------|-------------|
| Bruno Gomes | Compiladores, Reuso de Software, Tópicos em Engenharia de Software |
| Maria Aparecida da Silva Nascimento | Compiladores |
| Alan Diogo da Rocha Oliveira | Compiladores |
| Karlisson Henrique da Silva | Reuso de Software |

**Professor:** Dr. Arturo Hernandez Domínguez — UFAL / Instituto de Computação

## Pontos de variação (LPS)

| Ponto de variação | Variantes |
|-------------------|-----------|
| Modo de execução | Interpretador, Compilador |
| Back-end de compilação | C, C++, Rust, Assembly ARMv7, Python (extensão demo) |
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
├── docs/
│   ├── diagrams/             # Fontes Mermaid (.mmd)
│   ├── figures/              # PNG para relatório (diagramas + ui/)
│   └── VALIDATION.md
├── Relatório - Minipar 2026.1.pdf   # Relatório final (entrega)
├── report.tex                         # Fonte LaTeX do relatório
├── scripts/package-overleaf.sh
├── sources/examples/         # Fixtures 01–16
├── PROJECT_REQUIREMENTS.md   # Especificação das disciplinas
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
| ms-parallel-coord | 3006 | 🟡 POST /coordinate (workers socket) |

Pacote compartilhado: [`packages/minipar-core/`](packages/minipar-core/) — inclui `translation/` (Template Method).

Exemplos: [`sources/examples/`](sources/examples/) (01–16).

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

Validação automatizada: [`docs/VALIDATION.md`](docs/VALIDATION.md) · `./scripts/validate-all.sh`

Histórico no Postgres:

```bash
docker exec minipar-postgres psql -U minipar -d minipar \
  -c "SELECT id, status, target_variability FROM compilation_history ORDER BY created_at DESC LIMIT 5;"
```

## Entrega acadêmica

| Artefato | Caminho |
|----------|---------|
| **Relatório PDF (entrega)** | [**Relatório - Minipar 2026.1.pdf**](<Relatório - Minipar 2026.1.pdf>) |
| Fonte LaTeX | [report.tex](report.tex) · recompilar: `./scripts/build-pdf.sh` |
| Guia de instanciação / hotspots | [CREATING_AN_APPLICATION.md](CREATING_AN_APPLICATION.md) |
| Especificação do projeto | [PROJECT_REQUIREMENTS.md](PROJECT_REQUIREMENTS.md) |
| Validação | [docs/VALIDATION.md](docs/VALIDATION.md) |
