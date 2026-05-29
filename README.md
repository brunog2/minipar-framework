# MiniPar Framework 2026.1

Framework para compiladores e interpretadores da linguagem **MiniPar 2026.1** (OO + paralelismo real), organizado como **Linha de Produto de Software (LPS)** com arquitetura de **microsserviços**.

## Pontos de variação (LPS)

| Ponto de variação | Variantes |
|-------------------|-----------|
| Modo de execução | Interpretador, Compilador |
| Back-end de compilação | C, C++, Rust, Assembly ARMv7 |
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

## Estrutura do monorepo

```
minipar-framework/
├── frontend/             # Interface web (editor + seleção de variabilidade)
├── api-gateway/          # Orquestração central e persistência
├── database/init.sql     # Schema PostgreSQL
├── microservices/        # Especificações (README) de cada MS
└── docker-compose.yml    # Postgres + Gateway + Frontend
```

## Requisitos

- Node.js 20+
- Docker e Docker Compose
- (Futuro) GCC, toolchain ARM para back-ends reais

## Execução com Docker

```bash
cd minipar-framework
docker compose up --build
```

- Frontend: http://localhost:4200
- API Gateway: http://localhost:3000
- Health: http://localhost:3000/health
- PostgreSQL: `localhost:5432` (user/pass/db: `minipar`)

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

| `PIPELINE_MODE` | Comportamento |
|-----------------|---------------|
| `mock` (padrão) | Respostas simuladas; fluxo E2E sem microsserviços reais |
| `http` | Chama URLs em `MS_*_URL` (requer MS implementados) |

## Referências de reuso

Código base em `../code_references/`:

- **OO / AST:** `cl-minipar` (Java)
- **Codegen C/ARM:** `projeto_compiladores` (Python)

## Verificação E2E

```bash
curl http://localhost:3000/health

curl -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"sourceCode":"print(\"ok\")","targetVariability":"INTERPRETER","executionMode":"LOCAL"}'

docker exec minipar-postgres psql -U minipar -d minipar \
  -c "SELECT id, status, target_variability FROM compilation_history ORDER BY created_at DESC LIMIT 5;"
```

Interface em http://localhost:4200 — o nginx encaminha `/api/*` para o gateway.

## Roadmap

1. Implementar microsserviços conforme `microservices/*/README.md`
2. Teste de paralelismo (3 máquinas): QuickSort, matrizes, fatorial via sockets
3. Fractal (tapete de Sierpinski) em MiniPar OO — ver `../sources/Fractal-python.py`

## Entrega acadêmica

Ver [PROJECT_REQUIREMENTS.md](../PROJECT_REQUIREMENTS.md) — entrega **10 de junho**.
