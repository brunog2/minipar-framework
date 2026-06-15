# Atividades e responsabilidades — MiniPar Framework 2026.1

**Entrega:** 10 de junho de 2026  
**Última atualização:** 8 de junho de 2026  

**Ver também:** [SCHEDULE.md](./SCHEDULE.md) · [ROADMAP.md](./ROADMAP.md) · [COMPLIANCE_AUDIT.md](./COMPLIANCE_AUDIT.md) · [docs/WHAT_REMAINS.md](./docs/WHAT_REMAINS.md)

---

## Equipe

| Pessoa | Papel principal |
|--------|-----------------|
| **Bruno** | Integração (gateway, Docker, UI, Postgres), coordenação das 3 disciplinas |
| **Alan** | Parser/MS front-end, codegen C/Rust/ARM, paralelismo distribuído |
| **Karlisson** | Semântica, Template Method, interpretador, fractal |
| **Maria** | LPS/UML, metodologia ágil, relatório e slides |

---

## Product Backlog (integrado)

| ID | História / objetivo | Prioridade | Status |
|----|---------------------|------------|--------|
| PB-01 | Pipeline real parse → semântica → back-end via microsserviços | Alta | ✅ |
| PB-02 | Variabilidade LPS na UI (interpretador, C/C++/Rust/ARM, local/distribuído) | Alta | ✅ |
| PB-03 | Template Method para back-ends | Alta | ✅ |
| PB-04 | Teste professor: 3 máquinas via sockets | Alta | ✅ workers MiniPar + `14_distributed_menu` |
| PB-05 | Teste professor: fractal Sierpinski na UI | Alta | ✅ fonte + captura UI |
| PB-06 | Relatório integrado (3 disciplinas) | Alta | ✅ `report.tex` + `report.md` + figuras |
| PB-10 | Framework Arturo: instâncias + extensão Python | Alta | ✅ `applications/`, `PythonBackend`, docs |
| PB-07 | Apresentação ao vivo + vídeo backup | Alta | ⬜ |
| PB-08 | Semântica completa no `ms-semantic` | Média | ✅ `semantic_full.py` |
| PB-09 | `PAR` + sockets / Send-Receive na linguagem | Alta | ✅ broker TCP + `15_channels` |

---

## Sprint Backlogs (realizado vs. pendente)

### Sprint 0 — Kick-off (29–30/mai) ✅

- [x] Monorepo, Docker, Postgres, contrato AST
- [x] Diagrama arquitetura, esqueleto `report.tex`

### Sprint 1 — Fase 1 análise (29/mai–4/jun) ✅

- [x] `minipar-core`: lexer, parser, AST JSON
- [x] `ms-front-end`, `ms-semantic` (MVP)
- [x] Gateway + UI com pipeline HTTP
- [x] Exemplos `01–07`

### Sprint 2 — Fase 2 back-ends (2–5/jun) ✅ 🟡

- [x] `translation/` + Template Method
- [x] `ms-interpreter`, `ms-codegen-c` (`gcc -O2`)
- [x] `ms-codegen-rust` (MVP + `rustc` no container)
- [x] `ms-codegen-arm` (MVP)
- [x] `ms-codegen-python` (extensão demo) + exemplo `16`
- [x] Exemplos `08–16`
- [x] Validar `09_oo_new` com variante **C** (`validate-all.sh` E12)

### Sprint 3 — Fase 3 prova (5–7/jun) 🟡

- [x] `ms-parallel-coord` + 3 workers socket
- [x] Gateway `DISTRIBUTED_SOCKETS` + UI `distributedResults`
- [x] `13_sierpinski.minipar`, `14_distributed_menu.minipar`
- [x] `sequence-3-machines.mmd`
- [x] Checklist E2E — `./scripts/validate-all.sh` **15/15 PASS** (8/jun/2026)
- [x] Screenshots UI em `docs/figures/ui/` + `report.tex`/`report.md`
- [x] `applications/`, `CREATING_AN_APPLICATION.md`, `BANCA_NARRATIVE.md`

### Sprint 4 — Entrega acadêmica (7–10/jun) 🟡

- [x] UML/features como figuras no PDF (`docs/figures/*.png`)
- [x] `report.md` (Markdown com diagramas)
- [x] Compilar PDF final (`./scripts/build-pdf.sh` → `report.pdf`, `report-md.pdf`)
- [ ] Upload Overleaf opcional (`./scripts/package-overleaf.sh`)
- [ ] Slides + ensaio com [BANCA_NARRATIVE.md](./docs/BANCA_NARRATIVE.md)
- [ ] Ensaio geral + vídeo
- [ ] URLs finais GitHub/vídeo
- [ ] Entrega 10/jun

---

## Checklist E2E (preencher antes da banca)

Executar com `docker compose up --build` em `minipar-framework/`.

Executar: `./scripts/validate-all.sh` (com `docker compose up`). Guia: [`docs/VALIDATION.md`](./docs/VALIDATION.md).

| # | Atividade | Comando / UI | Esperado | OK? |
|---|-----------|--------------|----------|-----|
| E1 | Interpretador | Ex. `08` · INTERPRETER · LOCAL | `ok` | ✅ |
| E2 | OO | Ex. `09` · INTERPRETER · LOCAL | `woof` | ✅ |
| E3 | Fractal | Ex. `13` · INTERPRETER · LOCAL | matriz 27×27 | ✅ |
| E4 | 3 máquinas (legado) | Ex. `08` · INTERPRETER · DISTRIBUTED_SOCKETS | PC1 no output | ✅ |
| E5 | C + gcc | Ex. `11` · C · LOCAL | `Compiled with gcc -O2` | ✅ |
| E6 | Rust | Ex. `12` · RUST · LOCAL | `Compiled with rustc -O` | ✅ |
| E7 | Erro sintático | Ex. `05` | Parser error | ✅ |
| E8 | Erro semântico | Ex. `04` | Semantic error | ✅ |
| E9 | Extensão Python | Ex. `16` · PYTHON · LOCAL | `hello from Python backend` | ✅ |
| E10 | Menu MiniPar distribuído | Ex. `14` · INTERPRETER · DISTRIBUTED_SOCKETS | 3 linhas IP:porta | ✅ |
| E11 | Canais socket | Ex. `15` · INTERPRETER · LOCAL | `42` | ✅ |
| E12 | `09` + C | Ex. `09` · C · LOCAL | `woof` + gcc -O2 | ✅ |

Responsável por registrar resultados: **Bruno** (colar saídas ou prints na pasta `docs/evidence/` se criada).

---

## Atividades por microsserviço

| Microsserviço | Porta | Dono principal | Atividade atual |
|---------------|-------|----------------|-----------------|
| `api-gateway` | 3000 | Bruno | Manter `PIPELINE_*=http`; histórico PG |
| `ms-front-end` | 3001 | Alan | Parser OO + detecção erros sintáticos (E7) |
| `ms-semantic` | 3002 | Karlisson | `semantic_full.py` + `SemanticAnalyzer` |
| `ms-interpreter` | 3003 | Karlisson | OO + fractal + canais socket |
| `ms-codegen-c` | 3004 | Alan | Demo `gcc -O2`; OO em C |
| `ms-codegen-rust` | 3005 | Alan | `rustc` no Docker ✅ |
| `ms-parallel-coord` | 3006 | Alan | Demo 3 máquinas |
| `ms-codegen-python` | 3008 | Bruno | Extensão demo framework |
| `worker-*` | 9001–3 | Alan | MiniPar via `interpret_ast` |
| `frontend` | 4200 | Bruno | Templates ex. 13/14; Vercel |
| `postgres` | interno | Bruno | Logs compilação |

---

## Atividades de documentação

| Documento | Responsável | Status |
|-----------|-------------|--------|
| `COMPLIANCE_AUDIT.md` | Bruno | ✅ regenerado 15/15 PASS |
| `SCHEDULE.md` | Bruno | ✅ 2/jun |
| `ACTIVITIES.md` | Bruno | ✅ 2/jun |
| `ROADMAP.md` | Bruno | ✅ sincronizar após mudanças |
| `report.tex` / `report.pdf` | Todos | ✅ PDF 40 páginas (`./scripts/build-pdf.sh`) |
| `report.md` | Bruno | ✅ Markdown com diagramas |
| `docs/VALIDATION.md` | Bruno | ✅ guia + 13/13 PASS |
| `docs/WHAT_REMAINS.md` | Bruno | ✅ pós-conformidade |
| Diagramas → PNG | Maria/Bruno | ✅ `docs/figures/` |
| `README.md` | Bruno | ✅ links atualizados |

---

## O que não prometer na apresentação (sem novo código)

- Stack completa só pela URL Vercel (sem gateway/MS local)
- 3 PCs físicos separados (demo usa 3 containers Docker — topologia equivalente)

---

## Histórico

| Data | Alteração |
|------|-----------|
| 2026-06-08 | `build-pdf.sh`: `report.pdf` (40 pág.) + `report-md.pdf` + `overleaf-report.zip` |
| 2026-06-08 | Framework Arturo: `applications/`, Python, `report.md`, capturas UI |
