# Cronograma — MiniPar Framework 2026.1

**Entrega:** 10 de junho de 2026  
**Última atualização:** 2 de junho de 2026  
**Documentos relacionados:** [ROADMAP.md](./ROADMAP.md) · [ACTIVITIES.md](./ACTIVITIES.md) · [COMPLIANCE_AUDIT.md](./COMPLIANCE_AUDIT.md)

**Legenda:** `[x]` concluído · `[~]` parcial / em validação · `[ ]` pendente

**Fonte de verdade técnica:** código + [COMPLIANCE_AUDIT.md](./COMPLIANCE_AUDIT.md) (o que está ✅/🟡/❌ frente ao professor).

---

## Visão por fase (situação em 2/jun)

| Período | Marco | Status |
|---------|-------|--------|
| 29–30/mai | Kick-off, arquitetura, Docker base | ✅ |
| 29/mai–4/jun | Fase 1 — parse + semântica MVP | ✅ |
| 2–5/jun | Fase 2 — Template Method + back-ends | ✅ 🟡 (Rust/ARM MVP; semântica MVP no MS) |
| 5–7/jun | Fase 3 — 3 máquinas + fractal | 🟡 código; validar E2E + PDF |
| 3–10/jun | Fase 4 — relatório, UML, demo, entrega | 🟡 |
| 10/jun | **Entrega final** | ⬜ |

---

## 29–30/mai — Kick-off

- [x] (Bruno) Monorepo, `docker-compose`, Postgres, contrato AST
- [x] (Bruno) Diagrama arquitetura — `docs/diagrams/architecture.mmd`
- [x] (Bruno) `report.tex` esqueleto Overleaf
- [x] (Bruno) Mapa de reuso — `docs/diagrams/reuse-map.mmd`
- [ ] (Todos) Alinhar cópias locais / branches da equipe (organizacional)

---

## 29/mai–4/jun — Fase 1: Análise (Compiladores)

- [x] (Alan) `ms-front-end` — lexer + parser → AST JSON (`:3001`)
- [x] (Karlisson) `ms-semantic` — `semantic_json` MVP + symbolTable (`:3002`)
- [x] (Bruno) Gateway `PIPELINE_MODE=http` + UI Console (AST, símbolos, erros)
- [x] (Equipe) Fixtures `sources/examples/01–07`
- [x] (Bruno/Karlisson) Diagramas — `pipeline-sequence.mmd`, `frontend-semantic-flow.mmd`, `validation-cases.mmd`

**Pendente pós-Fase 1:** migrar `ms-semantic` para `semantic.py` completo (ver auditoria P1).

---

## 02/jun — Integração gateway + UI

- [x] (Bruno) `POST /api/v1/process`, histórico PostgreSQL
- [x] (Bruno) Frontend Angular + variabilidade LPS na UI
- [x] (Bruno) Deploy frontend [Vercel](https://minipar-framework.vercel.app/) (demo UI; E2E pleno = Docker local)

---

## 02–05/jun — Fase 2: Reuso e back-ends

- [x] (Karlisson) Template Method — `packages/minipar-core/minipar_core/translation/`
- [x] (Karlisson) `ms-interpreter` (`:3003`)
- [x] (Alan) `ms-codegen-c` + `gcc -O2` / `g++` (`:3004`)
- [x] (Alan) `ms-codegen-rust` MVP + **`rustc` no Dockerfile** (`:3005`)
- [x] (Alan) `ms-codegen-arm` MVP (`:3007`)
- [x] (Bruno) `PIPELINE_BACKEND_MODE=http` no gateway
- [x] (Bruno) Docker Compose — todos MS Fase 1–2 + healthchecks
- [x] (Karlisson/Alan) Diagramas — `template-method.mmd`, `codegen-c-flow.mmd`
- [x] (Equipe) Fixtures `sources/examples/08–12`
- [~] (Maria) Diagrama features LPS — `docs/diagrams/feature-tree.mmd` (arquivo existe; revisão PDF ⬜)

---

## 05–07/jun — Fase 3: Paralelismo e fractal

- [x] (Alan) `ms-parallel-coord` (`:3006`) + integração gateway
- [x] (Alan) Workers socket — `worker-quicksort` / `matrix` / `factorial` (`:9001–9003`)
- [x] (Bruno) Modo `DISTRIBUTED_SOCKETS` na UI + `distributedResults`
- [x] (Karlisson) `13_sierpinski.minipar` (fractal OO recursivo)
- [x] (Bruno) `14_distributed_menu.minipar` + template na UI
- [x] (Alan) `docs/diagrams/sequence-3-machines.mmd`
- [~] (Equipe) **Validar E2E** fractal + 3 máquinas (`docker compose up --build`)
- [~] (Maria/Equipe) Screenshots fractal + menu distribuído no `report.tex`
- [ ] (Equipe) `SendStmt` / `ReceiveStmt` no parser (opcional; não bloqueia demo atual)

**Ressalvas (auditoria):** teste 3 máq. usa Python nos workers, não MiniPar; `PAR` local usa threads, não sockets.

---

## 07–10/jun — Fase 4: Relatório, deploy e entrega

### Relatório (Overleaf)

- [~] (Bruno) Introdução, arquitetura, implementação, resultados Fase 1–3 (texto)
- [~] (Maria) Metodologia ágil — backlogs no `report.tex`
- [~] (Alan + Karlisson) BNF OO extrato no `report.tex`
- [~] (Maria) UML — `uml-use-cases.mmd`, `uml-components.mmd`, `uml-classes-framework.mmd` → **exportar para PDF**
- [ ] (Maria + equipe) Prints: fractal, 3 máquinas, pipeline steps
- [ ] (Bruno) URLs finais GitHub e vídeo (substituir placeholders)
- [ ] (Todos) Revisão PDF — **08/jun**

### Apresentação

- [ ] (Bruno + Maria + Alan + Karlisson) Slides — **07–08/jun**
- [ ] (Todos) Roteiro demo — ver [COMPLIANCE_AUDIT.md § 9](./COMPLIANCE_AUDIT.md#9-roteiro-de-demo-recomendado-10jun)
- [ ] (Todos) Ensaio com Docker + ensaio geral — **08–09/jun**
- [ ] (Todos) Vídeo backup — **09/jun**
- [ ] (Todos) **Entrega 10/jun**

### Deploy

- [x] (Bruno) Frontend Vercel
- [~] (Bruno) Gateway em produção (opcional; demo principal = Docker local)

---

## Calendário dia a dia (3–10/jun) — plano restante

| Dia | Foco principal | Responsáveis |
|-----|----------------|--------------|
| **3/jun** | E2E Fase 3 (`13`, `14`); alinhar docs | Bruno, Alan, Karlisson |
| **4/jun** | Screenshots UI; UML no PDF | Maria, Karlisson |
| **5/jun** | Texto resultados + LPS no `.tex` | Maria, equipe |
| **6/jun** | Validar `09` com C; polir Docker | Alan, Bruno |
| **7/jun** | Slides + sequência 3 máq. no relatório | Todos |
| **8/jun** | Fechar PDF + ensaio demo | Todos |
| **9/jun** | Vídeo backup | Todos |
| **10/jun** | **Entrega** | Todos |

---

## Dependências (caminho crítico)

```
kick-off → ms-front-end → ms-semantic → gateway http
    → Template Method → back-ends → ms-parallel-coord + fractal
    → validação E2E + relatório + apresentação → entrega 10/jun
```

| Demanda | Depende de | Status |
|---------|------------|--------|
| Back-ends | semântica + AST | ✅ |
| Fase 3 coord | gateway http | ✅ código |
| Fractal na UI | interpretador | ✅ código; 🟡 E2E |
| Relatório resultados | E2E + prints | ⬜ |
| PDF / slides | relatório + demo | ⬜ |

---

## Diagramas — quem e status

| Pessoa | Diagrama | Status |
|--------|----------|--------|
| Bruno | `architecture.mmd`, `pipeline-sequence.mmd` | ✅ |
| Karlisson | `frontend-semantic-flow.mmd`, `template-method.mmd` | ✅ |
| Alan | `codegen-c-flow.mmd`, `sequence-3-machines.mmd` | ✅ |
| Maria | `feature-tree.mmd`, `uml-*.mmd` | ✅ no repo; ⬜ figuras no PDF |
| Karlisson + Maria | `reuse-map.mmd` | ✅ |

Versionar em **`docs/diagrams/`**; exportar PNG/SVG para Overleaf.

---

## Histórico

| Data | Alteração |
|------|-----------|
| 2026-06-02 | Cronograma atualizado alinhado ao código e [COMPLIANCE_AUDIT.md](./COMPLIANCE_AUDIT.md) |
