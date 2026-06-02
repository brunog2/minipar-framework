# Atividades e responsabilidades — MiniPar Framework 2026.1

**Entrega:** 10 de junho de 2026  
**Última atualização:** 2 de junho de 2026  

**Ver também:** [SCHEDULE.md](./SCHEDULE.md) (datas) · [ROADMAP.md](./ROADMAP.md) (entregas técnicas) · [COMPLIANCE_AUDIT.md](./COMPLIANCE_AUDIT.md) (conformidade vs. requisitos do professor)

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
| PB-04 | Teste professor: 3 máquinas via sockets | Alta | 🟡 infra ✅; MiniPar nos workers ❌ |
| PB-05 | Teste professor: fractal Sierpinski na UI | Alta | 🟡 fonte ✅; E2E + print PDF |
| PB-06 | Relatório Overleaf integrado (3 disciplinas) | Alta | 🟡 |
| PB-07 | Apresentação ao vivo + vídeo backup | Alta | ⬜ |
| PB-08 | Semântica completa no `ms-semantic` | Média | ⬜ |
| PB-09 | `PAR` + sockets / Send-Receive na linguagem | Baixa* | ❌ |

\*Baixa para entrega 10/jun se narrativa de demo for honesta (ver auditoria).

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
- [x] Exemplos `08–12`
- [ ] Validar rotineiramente `09_oo_new` com variante **C**

### Sprint 3 — Fase 3 prova (5–7/jun) 🟡

- [x] `ms-parallel-coord` + 3 workers socket
- [x] Gateway `DISTRIBUTED_SOCKETS` + UI `distributedResults`
- [x] `13_sierpinski.minipar`, `14_distributed_menu.minipar`
- [x] `sequence-3-machines.mmd`
- [ ] Checklist E2E assinado pela equipe (tabela abaixo)
- [ ] Screenshots no `report.tex`

### Sprint 4 — Entrega acadêmica (7–10/jun) ⬜

- [ ] UML/features como figuras no PDF
- [ ] Slides + roteiro demo
- [ ] Ensaio geral + vídeo
- [ ] URLs finais GitHub/vídeo
- [ ] Entrega 10/jun

---

## Checklist E2E (preencher antes da banca)

Executar com `docker compose up --build` em `minipar-framework/`.

| # | Atividade | Comando / UI | Esperado | OK? |
|---|-----------|--------------|----------|-----|
| E1 | Interpretador | Ex. `08` · INTERPRETER · LOCAL | `ok` | ☐ |
| E2 | OO | Ex. `09` · INTERPRETER · LOCAL | `woof` | ☐ |
| E3 | Fractal | Ex. `13` · INTERPRETER · LOCAL | matriz 27×27 | ☐ |
| E4 | 3 máquinas | qualquer fonte · INTERPRETER · DISTRIBUTED_SOCKETS | PC1–PC3 no output | ☐ |
| E5 | C + gcc | Ex. `11` · C · LOCAL | `Compiled with gcc -O2` | ☐ |
| E6 | Rust | `Main.run` + println · RUST · LOCAL | `Compiled with rustc -O` | ☐ |
| E7 | Erro sintático | Ex. `05` | Parser error no Console | ☐ |
| E8 | Erro semântico | Ex. `04` | Semantic error | ☐ |

Responsável por registrar resultados: **Bruno** (colar saídas ou prints na pasta `docs/evidence/` se criada).

---

## Atividades por microsserviço

| Microsserviço | Porta | Dono principal | Atividade atual |
|---------------|-------|----------------|-----------------|
| `api-gateway` | 3000 | Bruno | Manter `PIPELINE_*=http`; histórico PG |
| `ms-front-end` | 3001 | Alan | Manter parser OO; Send/Receive futuro |
| `ms-semantic` | 3002 | Karlisson | Evoluir para `semantic.py` (P1 auditoria) |
| `ms-interpreter` | 3003 | Karlisson | Demo OO + fractal |
| `ms-codegen-c` | 3004 | Alan | Demo `gcc -O2`; OO em C |
| `ms-codegen-rust` | 3005 | Alan | `rustc` no Docker ✅ |
| `ms-parallel-coord` | 3006 | Alan | Demo 3 máquinas |
| `ms-codegen-arm` | 3007 | Alan | MVP documentado |
| `worker-*` | 9001–3 | Alan | Socket servers |
| `frontend` | 4200 | Bruno | Templates ex. 13/14; Vercel |
| `postgres` | interno | Bruno | Logs compilação |

---

## Atividades de documentação

| Documento | Responsável | Status |
|-----------|-------------|--------|
| `COMPLIANCE_AUDIT.md` | Bruno | ✅ mantido com código |
| `SCHEDULE.md` | Bruno | ✅ 2/jun |
| `ACTIVITIES.md` | Bruno | ✅ 2/jun |
| `ROADMAP.md` | Bruno | ✅ sincronizar após mudanças |
| `report.tex` | Todos | 🟡 |
| Diagramas → PDF | Maria | ⬜ |
| `README.md` | Bruno | 🟡 manter links |

---

## O que não prometer na apresentação (sem novo código)

- `PAR` da linguagem disparando processos com sockets
- QuickSort / matriz / fatorial **escritos em MiniPar** nos workers
- Semântica “completa” de tipos se ainda for MVP no MS
- Stack completa só pela URL Vercel (sem gateway/MS)

---

## Histórico

| Data | Alteração |
|------|-----------|
| 2026-06-02 | Criação — atividades alinhadas ao cronograma e auditoria |
