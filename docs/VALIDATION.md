# Guia de validação — MiniPar Framework 2026.1

**Última execução:** 8 de junho de 2026 — **15/15 PASS**  
**Evidência:** [`docs/evidence/validation-results.json`](../docs/evidence/validation-results.json)

---

## Validação automática (recomendado)

```bash
cd minipar-framework
docker compose up --build -d
# aguardar healthchecks (~45s)
./scripts/validate-all.sh
```

O script:

1. Testa `minipar-core` localmente (canais, OO, codegen C).
2. Se o gateway estiver em `http://localhost:3000`, executa os casos HTTP E2E.
3. Grava JSON em `docs/evidence/validation-results.json`.

Smoke rápido (subset):

```bash
./scripts/e2e-smoke.sh
```

---

## Pré-requisitos

| Item | Comando / verificação |
|------|----------------------|
| Docker + Compose | `docker compose version` |
| Stack no ar | `curl -s http://localhost:3000/health` |
| UI (opcional) | http://localhost:4200 |
| Python 3 (scripts locais) | `python3 --version` |

Variáveis úteis:

```bash
export MINIPAR_API=http://localhost:3000   # padrão do validate-all.sh
```

---

## Matriz por fase do plano de conformidade

| Fase | ID | O quê validar | Como | Esperado |
|------|-----|---------------|------|----------|
| **0** | GW | Gateway saudável | `curl http://localhost:3000/health` | HTTP 200 |
| **1** | E1 | Interpretador básico | Ex. `08` · INTERPRETER · LOCAL | `ok` |
| **1** | E7 | Erro sintático | Ex. `05` · INTERPRETER · LOCAL | `Parser error` |
| **1–2** | E11 | Canais socket | Local: `15_channels.minipar` | `42` |
| **2** | E2 | Interpretador OO | Ex. `09` · INTERPRETER · LOCAL | `woof` |
| **2** | E6 | Codegen Rust | Ex. `12` · RUST · LOCAL | `rustc` + stdout |
| **3** | E3 | Fractal Sierpinski | Ex. `13` · INTERPRETER · LOCAL | matriz `*`/`.` |
| **3** | E4 | Modo distribuído (legado) | Ex. `08` · DISTRIBUTED_SOCKETS | PC1–PC3 |
| **3** | E10 | Menu MiniPar distribuído | Ex. `14` · DISTRIBUTED_SOCKETS | IP:porta × 3 |
| **4** | E8 | Erro semântico | Ex. `04` · INTERPRETER · LOCAL | erro semântico |
| **5** | E5 | Codegen C | Ex. `11` · C · LOCAL | `gcc -O2` |
| **5** | E12 | OO + C | Ex. `09` · C · LOCAL | `woof` + gcc |
| **6** | E9 | Extensão Python | Ex. `16` · PYTHON · LOCAL | `hello from Python backend` |
| **6** | — | Health agregado MS | `GET /api/v1/services/health` | todos `ok` |
| **6** | — | Variantes LPS | `GET /api/v1/variants` | lista INTERPRETER, C, … |
| **6** | — | Recomendações | `GET /api/v1/recommendations` | JSON com `suggestedVariability` |

---

## Validação manual por componente

### 1. Canais e broker TCP (Fases 1–2)

**Arquivo:** `sources/examples/15_channels.minipar`

```bash
cd packages/minipar-core
PYTHONPATH=. python3 -c "
from minipar_core.pipeline import parse_source
from minipar_core.translation.interpreter import interpret_ast
src = open('../../sources/examples/15_channels.minipar').read()
ast, _ = parse_source(src)
print(interpret_ast(ast).output)
"
```

**Esperado:** `42`

**Código:** `packages/minipar-core/minipar_core/channels/socket_channel.py`, `exec_par` em `interpreter.py`.

### 2. Erro sintático (E7)

**Arquivo:** `sources/examples/05_parse_extends_missing.minipar` — `extends` sem superclasse.

**Esperado:** `"success": false`, mensagem `Parser error`.

### 3. Semântica completa (Fase 4)

**Erro esperado** (`04_semantic_extends_unknown.minipar`):

```bash
curl -s -X POST http://localhost:3000/api/v1/process \
  -H 'Content-Type: application/json' \
  -d '{"sourceCode":"'"$(cat sources/examples/04_semantic_extends_unknown.minipar)"'","targetVariability":"INTERPRETER","executionMode":"LOCAL"}' \
  | python3 -m json.tool
```

**Esperado:** `"success": false` com mensagem semântica.

**Código:** `ms-semantic` → `semantic_full.py` → `SemanticAnalyzer`.

### 4. Workers MiniPar + menu distribuído (Fase 3)

**Workers:** `microservices/parallel-workers/sources/worker_*.minipar`

```bash
docker compose ps | grep worker
curl -s http://localhost:3000/api/v1/process \
  -H 'Content-Type: application/json' \
  -d @- <<'EOF'
{"sourceCode":"class Main { void run() { c_channel ch1(\"worker-quicksort\", 9001); receive(ch1, r); println(r); } }","targetVariability":"INTERPRETER","executionMode":"DISTRIBUTED_SOCKETS"}
EOF
```

**Menu completo:** `14_distributed_menu.minipar` — três `c_channel` + `par { receive … }`.

### 5. Codegen C com runtime PAR (Fase 5)

```bash
PYTHONPATH=packages/minipar-core python3 -c "
from minipar_core.pipeline import parse_source
from minipar_core.translation import generate_c
ast, _ = parse_source(open('sources/examples/11_codegen_c.minipar').read())
print(generate_c(ast).output)
"
```

**Esperado:** compilação `gcc -O2` e stdout do programa.

**Runtime:** `packages/minipar-core/minipar_core/runtime/minipar_rt.c`

### 6. Codegen Rust (E6)

**Arquivo:** `sources/examples/12_codegen_rust_stub.minipar` · variante **RUST** · LOCAL.

**Esperado:** `Compiled with rustc -O` e `hello rust`.

### 7. LPS — variantes, health e recomendações (Fase 6)

```bash
curl -s http://localhost:3000/api/v1/variants | python3 -m json.tool
curl -s http://localhost:3000/api/v1/services/health | python3 -m json.tool
curl -s http://localhost:3000/api/v1/recommendations | python3 -m json.tool
```

**UI:** painel **Microsserviços** na sidebar (atualiza a cada 30s via gateway).

```bash
curl -s http://localhost:3000/api/v1/variants | python3 -m json.tool
curl -s http://localhost:3000/api/v1/recommendations | python3 -m json.tool
```

**UI:** painel de status dos microsserviços na sidebar do workspace.

---

## Validação via UI

1. Abrir http://localhost:4200
2. Selecionar exemplo no painel (ex. `13_sierpinski`)
3. Escolher variante (INTERPRETER / C / PYTHON) e modo (LOCAL / DISTRIBUTED_SOCKETS)
4. Executar e conferir Console + painel de serviços

Capturas de referência: `docs/figures/ui/`.

---

## Troubleshooting

| Sintoma | Causa provável | Ação |
|---------|----------------|------|
| HTTP 500 em todo pipeline | `ms-semantic` com AST sem `line` | Rebuild: `docker compose build ms-semantic && docker compose up -d ms-semantic` |
| E10 falha semântica `r1/r2/r3` | escopo `par` | Corrigido em `semantic.py` (receive visível após `par`) |
| Gateway não responde | stack ainda subindo | `docker compose ps`, aguardar `healthy` |
| E4/E10 timeout | workers offline | `docker compose up -d worker-quicksort worker-matrix worker-factorial` |
| Testes locais OK, HTTP falha | imagem Docker antiga | `docker compose build --no-cache ms-interpreter ms-semantic api-gateway` |

---

## Registro de evidências

Após validação bem-sucedida:

```bash
./scripts/validate-all.sh
./scripts/build-pdf.sh    # report.pdf + report-md.pdf + overleaf-report.zip
```

Evidências adicionais:

- `docs/evidence/15_channels_socket.txt`
- Screenshots em `docs/figures/ui/`
- Histórico PostgreSQL via gateway (`compilation_history`)

---

## Referências

- Guia de instanciação: [`CREATING_AN_APPLICATION.md`](../CREATING_AN_APPLICATION.md)
- Relatório: [`report.tex`](../report.tex)
- Especificação: [`PROJECT_REQUIREMENTS.md`](../PROJECT_REQUIREMENTS.md)
