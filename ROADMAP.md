# MiniPar Framework 2026.1 — Roadmap e status do projeto

**Referências:** [PROJECT_REQUIREMENTS.md](./PROJECT_REQUIREMENTS.md) · [COMPLIANCE_AUDIT.md](./COMPLIANCE_AUDIT.md) · [SCHEDULE.md](./SCHEDULE.md) · [README.md](./README.md)  
**Entrega:** 10 de junho de 2026  
**Última atualização:** 2 de junho de 2026 (auditoria de conformidade documentada)

Legenda: ✅ concluído · 🟡 parcial / MVP · ⬜ pendente

---

## Panorama executivo

| Fase | Período (SCHEDULE) | Status geral |
|------|-------------------|--------------|
| **Kick-off / infra** | 29–30/mai | ✅ |
| **Fase 1** — Análise estática (parse + semântica) | 29/mai–4/jun | ✅ |
| **Fase 2** — Back-ends + Template Method + reuso | 2–5/jun | ✅ (com limitações documentadas) |
| **Fase 3** — Testes “de prova” (3 máquinas + fractal) | 5–7/jun | 🟡 ver [COMPLIANCE_AUDIT.md](./COMPLIANCE_AUDIT.md) |
| **Fase 4** — Entrega acadêmica (relatório, LPS, demo) | 3–10/jun | 🟡 |

**Situação atual:** o pipeline E2E real funciona (`PIPELINE_MODE=http`, `PIPELINE_BACKEND_MODE=http`). A UI, o gateway, o Postgres e **7 microsserviços** estão integrados no Docker Compose. O gargalo migrou de “não há compilador” para **requisitos de demonstração final** (paralelismo distribuído, fractal, documentação LPS/UML completa).

---

## Mapa: requisitos do professor → fases

| Requisito (`PROJECT_REQUIREMENTS.md`) | Onde entra | Status |
|--------------------------------------|------------|--------|
| Linguagem MiniPar 2026.1 **OO** (classes, `extends`, `new`, métodos) | Fase 1 (parse/AST) + Fase 2 (interpretador) | 🟡 Ver seção [OO](#orientação-a-objetos-oo--escopo-por-fase) |
| Pipeline: léxico, sintático, semântico, tabela de símbolos | Fase 1 | ✅ |
| Geradores de código (C/C++/Rust/ARM + interpretador) | Fase 2 | 🟡 Interpretador + C MVP; Rust/ARM MVP |
| `gcc -O2` para C/C++ | Fase 2 (`ms-codegen-c`) | ✅ |
| **Template Method** + hotspots | Fase 2 (`minipar-core/translation/`) | ✅ |
| Microsserviços REST + JSON + API Gateway | Fases 0–2 | ✅ (NestJS, não Spring) |
| LPS documentada (variabilidade → MS) | Fase 4 (Maria) | 🟡 UI + gateway ok; diagrama features ⬜ |
| **Paralelismo real** (`PAR` + threads + **sockets**) | Fase 3 | 🟡 infra socket ✅; `PAR` MiniPar ❌ — [auditoria](./COMPLIANCE_AUDIT.md#1-compiladores-minipar-20261-oo) |
| **Teste 3 máquinas** (QuickSort, matrizes, fatorial) | Fase 3 | 🟡 workers socket ✅; MiniPar nos workers ❌ |
| **Fractal Sierpinski** (matriz na UI) | Fase 3 | 🟡 fonte ✅; validar E2E + print PDF |
| Relatório Overleaf + GitHub + apresentação | Fase 4 | 🟡 `report.tex` parcial |

---

## Kick-off e infraestrutura (29–30/mai) — ✅

| Item | Responsável | Status | Evidência |
|------|-------------|--------|-----------|
| Monorepo, estrutura de pastas | Bruno | ✅ | `frontend/`, `api-gateway/`, `packages/`, `microservices/` |
| `docker-compose.yml` + Postgres | Bruno | ✅ | Rede `minipar`, histórico `compilation_history` |
| Contrato AST JSON | Equipe | ✅ | `microservices/_AST_CONTRACT.md` |
| Specs README de cada MS | Equipe | ✅ | `microservices/ms-*/README.md` |
| Diagrama arquitetura | Bruno | ✅ | `docs/diagrams/architecture.mmd` |
| Mapa de reuso | Karlisson + Maria | ✅ | `docs/diagrams/reuse-map.mmd` |
| Frontend Angular + LPS na UI | Bruno | ✅ | Deploy [Vercel](https://minipar-framework.vercel.app/) |
| API Gateway NestJS | Bruno | ✅ | `POST /api/v1/process`, histórico PG |
| Estrutura base `report.tex` | Bruno | 🟡 | Seções Fase 1–2 preenchidas; BNF/UML placeholders |

---

## Fase 1 — Análise estática (29/mai–4/jun) — ✅

**Objetivo:** pipeline real até semântica; UI e gateway com AST e `symbolTable` reais.

### Entregas técnicas

| # | Entrega | Responsável | Status | Detalhe |
|---|---------|-------------|--------|---------|
| 1.1 | `packages/minipar-core` — lexer, parser, AST OO | Alan / equipe | ✅ | `lexer.py`, `parser.py`, `ast_nodes.py` |
| 1.2 | Serialização AST → JSON | Equipe | ✅ | `ast_json.py` |
| 1.3 | Análise semântica MVP | Karlisson | ✅ | `semantic_json.py` (classes, `extends`, duplicatas) |
| 1.4 | **`ms-front-end`** FastAPI `:3001` | Alan | ✅ | `POST /parse` |
| 1.5 | **`ms-semantic`** FastAPI `:3002` | Karlisson | ✅ | `POST /analyze` |
| 1.6 | Gateway `PIPELINE_MODE=http` | Bruno | ✅ | `pipeline.service.ts` → MS reais |
| 1.7 | Integração Docker + UI E2E | Bruno | ✅ | nginx proxy, botão **Executar**, Console |
| 1.8 | Fixtures de validação | Equipe | ✅ | `sources/examples/01–07` |
| 1.9 | Diagramas pipeline / semântica | Bruno / Karlisson | ✅ | `pipeline-sequence.mmd`, `frontend-semantic-flow.mmd`, `validation-cases.mmd` |

### Critérios de aceite Fase 1

- [x] `curl` e UI retornam AST real (`ClassDecl`, etc.)
- [x] Erros de parse e semântica exibidos no Console
- [x] `pipelineSteps`: `ms-front-end: parse`, `ms-semantic: analyze` (sem mock)

### Limitações conhecidas (Fase 1)

- Semântica completa (`semantic.py`) existe mas o MS usa **`semantic_json` MVP**
- `SendStmt` / `ReceiveStmt` no contrato AST — **não implementados** no parser (Fase 3)

---

## Fase 2 — Back-ends e reuso (2–5/jun) — ✅ 🟡

**Objetivo:** Template Method, interpretador real, codegen C com `gcc -O2`, Rust/ARM MVP.

### Entregas técnicas

| # | Entrega | Responsável | Status | Detalhe |
|---|---------|-------------|--------|---------|
| 2.1 | **`translation/`** + Template Method | Karlisson | ✅ | `AbstractBackendTranslator`, `TranslationResult` |
| 2.2 | `ast_from_json.py` | Karlisson | ✅ | Deserialização para MS |
| 2.3 | TAC + `tac_codegen` (port + OO mínimo) | Alan + Karlisson | ✅ | `tac.py`, `tac_codegen.py` |
| 2.4 | **`ms-interpreter`** `:3003` | Karlisson | ✅ | OO MVP: `new`, métodos, `Main.run()`, `seq`/`par` (threads) |
| 2.5 | **`ms-codegen-c`** `:3004` | Alan | ✅ | `gcc -O2` / `g++`; `println` global + `Main.run()` |
| 2.6 | **`ms-codegen-rust`** `:3005` | Alan | 🟡 MVP | Gera Rust; `rustc` opcional |
| 2.7 | **`ms-codegen-arm`** `:3007` | Alan | 🟡 MVP | Gera `.s` ARMv7; toolchain opcional |
| 2.8 | `PIPELINE_BACKEND_MODE=http` | Bruno | ✅ | Gateway chama MS 3003–3007 |
| 2.9 | Docker Compose — todos MS análise + back-end | Bruno | ✅ | Rede `minipar`, wait-for-postgres no gateway |
| 2.10 | Diagramas Template Method / codegen | Karlisson / Alan | ✅ | `template-method.mmd`, `codegen-c-flow.mmd` |
| 2.11 | Fixtures Fase 2 | Equipe | ✅ | `sources/examples/08–12` |
| 2.12 | `report.tex` § Reuso + Resultados Fase 2 | Equipe | 🟡 | Template Method ok; BNF/UML parcial |

### Critérios de aceite Fase 2

- [x] Interpretador: `class Main { void run() { println("ok"); } }` → output `ok`
- [x] C: `println("hello")` global e `Main.run()` compilam com `gcc -O2`
- [x] Rust/ARM: geram artefato ou mensagem clara se toolchain ausente
- [x] Template Method documentado (código + diagrama + relatório)
- [ ] **OO completo no codegen C/C++** — explicitamente **fora** do fechamento Fase 2 (ver abaixo)

### Limitações conhecidas (Fase 2)

| Área | O que funciona | O que falta |
|------|----------------|-------------|
| **Interpretador** | `new`, chamada de método, herança básica, `par`/`seq` local | `SuperCall`, canais TCP, I/O avançado |
| **Codegen C/C++** | `println`, `Main.run()`, defs de método como funções C | `new` + `d.bark()` → **não compila** ainda |
| **Semântica** | MVP JSON | Tipos completos, despacho dinâmico |
| **Testes unitários** | — | Fora do escopo acordado |

---

## Orientação a objetos (OO) — escopo por fase

### Precisa de OO completo para a entrega?

**Sim, parcialmente** — o `PROJECT_REQUIREMENTS.md` exige OO na linguagem e no framework, mas com nuances:

| Exigência OO | Obrigatório para nota? | Onde demonstrar | Status |
|--------------|------------------------|-----------------|--------|
| Parser/AST OO (`class`, `extends`, `new`, métodos) | Sim | Fase 1 + relatório BNF/AST | ✅ |
| Execução OO (`new`, métodos, herança) | Sim | **Interpretador** + demo UI | ✅ MVP |
| Compilação OO (`new` → C, virtual dispatch) | Desejável / “alta performance” | Back-end **C** | ⬜ Fase 2.5+ |
| `PAR` com **threads** | Sim (Compiladores) | Interpretador local | 🟡 threads sim; **sockets não** |
| `PAR` + **sockets** entre processos | Sim (requisito “paralelismo real”) | Fase 3 | ⬜ |
| Fractal **recursivo OO** | Sim (teste obrigatório) | Fase 3 | ⬜ |

### Em qual fase implementar OO completo?

| Camada | Fase | Situação |
|--------|------|----------|
| AST + parse OO | **Fase 1** | ✅ Feito |
| Semântica OO rica | **Fase 2.5** (refino) ou paralelo à Fase 3 | 🟡 MVP; migrar para `semantic.py` se bloquear fractal |
| **Runtime OO completo** (demo principal) | **Fase 2** | ✅ Interpretador — **usar este back-end na apresentação OO** |
| **Codegen OO** (`new`, métodos, structs) | **Fase 2.5** (3–6/jun, não nomeada no SCHEDULE) | ⬜ Próximo incremento antes da entrega se quiser demo C com `new` |
| OO + **sockets** + 3 máquinas | **Fase 3** | ⬜ |
| OO **recursivo** (fractal) | **Fase 3** | ⬜ |

**Recomendação para a entrega (10/jun):**

1. **Demo OO:** variabilidade **Interpretador** — exemplos `08`, `09`, `10`.
2. **Demo compilador:** variabilidade **C** — `println` global, `Main.run()`, `11_codegen_c`.
3. **Não prometer** `new Dog(); d.bark()` no gcc até implementar Fase 2.5.
4. **Fractal + 3 máquinas** exigem OO recursivo + rede — **Fase 3** (prioridade máxima agora).

---

## Fase 3 — Requisitos “de prova” (5–7/jun) — ⬜

| # | Entrega | Responsável | Status | Notas |
|---|---------|-------------|--------|-------|
| 3.1 | **`ms-parallel-coord`** `:3006` | Alan | ⬜ | Spec em `microservices/ms-parallel-coord/README.md` |
| 3.2 | Modo `DISTRIBUTED_SOCKETS` E2E | Alan + Bruno | ⬜ | UI já tem o toggle; gateway tem stub de rota |
| 3.3 | Worker 1 — QuickSort | Alan | ⬜ | Container/processo + socket |
| 3.4 | Worker 2 — multiplicação de matrizes | Alan | ⬜ | idem |
| 3.5 | Worker 3 — fatorial | Alan | ⬜ | idem |
| 3.6 | Menu coordenador + resultados na UI | Bruno | ⬜ | |
| 3.7 | **Fractal Sierpinski** MiniPar OO | Karlisson | ⬜ | Ref. `../sources/Fractal-python.py` |
| 3.8 | Saída matriz `.`/`*` no Console | Karlisson | ⬜ | Screenshot no relatório |
| 3.9 | Diagrama sequência 3 máquinas | Alan | ⬜ | SCHEDULE |
| 3.10 | Canais / `SendStmt` / `ReceiveStmt` (se necessário) | Equipe | ⬜ | Parser + runtime |

**Mitigação:** 3 containers na mesma rede Docker = “3 computadores” para a demo.

---

## Fase 4 — Entrega acadêmica (3–10/jun) — 🟡

| # | Entrega | Responsável | Status |
|---|---------|-------------|--------|
| 4.1 | Diagrama **features LPS** + binding → MS | Maria | ⬜ |
| 4.2 | UML: casos de uso, componentes, classes | Maria | ⬜ |
| 4.3 | BNF OO completa no relatório | Alan + Karlisson | ⬜ placeholder |
| 4.4 | `report.tex` — Metodologia | Maria + Bruno | 🟡 |
| 4.5 | `report.tex` — Resultados (prints fractal + 3 máq.) | Maria + Alan + Karlisson | ⬜ depende Fase 3 |
| 4.6 | Fechar PDF Overleaf | Todos | ⬜ 8/jun |
| 4.7 | Slides apresentação | Bruno + Maria + Alan + Karlisson | ⬜ 7–8/jun |
| 4.8 | Roteiro + ensaio demo ao vivo | Todos | ⬜ 8–9/jun |
| 4.9 | Vídeo backup | Todos | ⬜ 9/jun |
| 4.10 | Repositório GitHub público | Bruno | 🟡 |
| 4.11 | URLs no relatório (repo + vídeo) | Bruno | ⬜ placeholders |

### Diagramas versionados (`docs/diagrams/`)

| Arquivo | Status |
|---------|--------|
| `architecture.mmd` | ✅ |
| `pipeline-sequence.mmd` | ✅ |
| `frontend-semantic-flow.mmd` | ✅ |
| `validation-cases.mmd` | ✅ |
| `template-method.mmd` | ✅ |
| `codegen-c-flow.mmd` | ✅ |
| `reuse-map.mmd` | ✅ |
| Feature tree LPS | ⬜ Maria |
| Sequência 3 máquinas | ⬜ Alan |
| UML casos de uso | ⬜ Maria |

---

## Cronograma SCHEDULE vs realizado (2/jun)

| Prazo | Tarefa SCHEDULE | Situação real |
|-------|-----------------|---------------|
| 29–30/mai | Board, mapa reuso, arquitetura | ✅ |
| 29/mai–02/jun | `ms-front-end` | ✅ (entregue na Fase 1) |
| 30/mai–02/jun | `ms-semantic` | ✅ |
| 02/jun | Integrar gateway + UI | ✅ |
| 02–04/jun | Template Method + pacote compartilhado | ✅ |
| 03–05/jun | `ms-interpreter` | ✅ |
| 03–05/jun | `ms-codegen-c` | ✅ |
| 04–05/jun | Rust + ARM MVP | ✅ |
| 04–05/jun | LPS features (Maria) | ⬜ |
| 05–07/jun | Paralelismo 3 máquinas | ⬜ |
| 06–07/jun | Fractal + UI | ⬜ |
| 06–07/jun | Docker Compose completo | ✅ |
| 07–10/jun | Relatório, slides, entrega | 🟡 em andamento |

---

## Microsserviços — tabela consolidada

| Serviço | Porta | Fase | Status | Rota |
|---------|-------|------|--------|------|
| ms-front-end | 3001 | 1 | ✅ | `POST /parse` |
| ms-semantic | 3002 | 1 | ✅ | `POST /analyze` |
| ms-interpreter | 3003 | 2 | ✅ | `POST /execute` |
| ms-codegen-c | 3004 | 2 | ✅ | `POST /generate` (gcc -O2) |
| ms-codegen-rust | 3005 | 2 | 🟡 MVP | `POST /generate` |
| ms-parallel-coord | 3006 | 3 | ⬜ | `POST /coordinate` |
| ms-codegen-arm | 3007 | 2 | 🟡 MVP | `POST /generate` |
| api-gateway | 3000 | 0–2 | ✅ | `POST /api/v1/process` |
| frontend | 4200 | 0–2 | ✅ | nginx → gateway |

---

## Checklist entrega 10/jun (`PROJECT_REQUIREMENTS.md`)

| Critério | Status |
|----------|--------|
| Pipeline real: léxico → sintático → semântico → back-end | ✅ |
| Template Method no código + relatório | ✅ |
| Interpretador com execução real | ✅ |
| Compilador C com `gcc -O2` | ✅ (subset procedural + `Main.run`) |
| Variabilidade LPS na UI (C, Rust, ARM, Interpretador) | ✅ |
| API Gateway + microsserviços REST/JSON | ✅ |
| **Teste paralelo 3 máquinas (sockets)** | ⬜ Fase 3 |
| **Fractal Sierpinski na interface** | ⬜ Fase 3 |
| Relatório Overleaf completo | 🟡 |
| GitHub + apresentação com demo ao vivo | 🟡 |

---

## Matriz de risco (atualizada)

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Fase 3 atrasada (fractal + 3 máq.) | **Alto** — requisitos obrigatórios do professor | Prioridade imediata; 3 containers = 3 máquinas |
| OO incompleto no **gcc** | Médio | Demo OO no **Interpretador**; documentar limitação no relatório |
| Semântica MVP insuficiente para fractal | Médio | Estender `semantic_json` ou usar `semantic.py` |
| Canais/sockets não no parser | Alto para Fase 3 | Implementar mínimo `Send`/`Receive` ou coordenador sem canal MiniPar |
| Relatório/UML atrasado (Maria) | Médio | Escrever com diagramas `.mmd` já prontos; resultados entram após Fase 3 |
| Gateway NestJS vs Spring sugerido | Baixo | Documentar decisão no relatório |
| Pouco tempo (8 dias) | Alto | Cortar paridade Rust/ARM; foco Interpretador + C + Fase 3 |

---

## Próximos passos imediatos (pós-Fase 2)

### Prioridade 1 — Fase 3 (5–7/jun)

1. **`ms-parallel-coord`** + 3 workers (Alan)  
2. **Fractal Sierpinski** MiniPar + saída na UI (Karlisson)  
3. Integrar `DISTRIBUTED_SOCKETS` no gateway (Bruno)

### Prioridade 2 — Fase 4 em paralelo (Maria + equipe)

4. Diagrama features LPS + UML  
5. Completar BNF e placeholders do `report.tex`  
6. Slides e roteiro de demo (Interpretador OO + C + fractal + 3 máq.)

### Prioridade 3 — Refino opcional (se sobrar tempo)

7. **Fase 2.5:** OO no codegen C (`new` → struct + chamada `Dog_bark()`)  
8. Semântica completa; testes unitários (se professor exigir)

---

## Plano sugerido dia a dia (3–10/jun)

| Dia | Bruno | Alan | Karlisson | Maria |
|-----|-------|------|-----------|-------|
| **3/jun** | Gateway + coord stub; compose workers | Início `ms-parallel-coord` | Fractal: AST + interpretador | Feature tree LPS |
| **4/jun** | UI resultados distribuídos | Workers QuickSort / matriz / fat | Fractal: matriz no Console | UML casos de uso |
| **5/jun** | E2E 3 máquinas | Fechar coord + sockets | Fractal + screenshots | Reuso + LPS no `.tex` |
| **6/jun** | Docker polish; deploy | Codegen OO (opcional) | Resultados fractal no relatório | UML componentes |
| **7/jun** | Slides infra + demo | Sequência 3 máq. no `.mmd` | Template Method / AST no `.tex` | Revisão PDF |
| **8/jun** | Ensaio geral | Ensaio demo técnica | Ensaio demo técnica | Fechar PDF |
| **9/jun** | Vídeo backup | — | — | — |
| **10/jun** | **Entrega** | **Entrega** | **Entrega** | **Entrega** |

---

## Como testar o que já está pronto

```bash
cd minipar-framework
docker compose up --build

# Interpretador OO
curl -s -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"sourceCode":"class Main { void run() { println(\"ok\"); } }","targetVariability":"INTERPRETER","executionMode":"LOCAL"}'

# Codegen C
curl -s -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"sourceCode":"println(\"hello MiniPar\");","targetVariability":"C","executionMode":"LOCAL"}'
```

UI: http://localhost:4200 — **Executar** · exemplos em [`sources/examples/README.md`](sources/examples/README.md).

---

## Resumo: OO completo — precisa? em qual fase?

| Pergunta | Resposta |
|----------|----------|
| **Precisa de OO para passar?** | Sim — parser, execução e fractal OO são exigidos. |
| **OO já está “completo”?** | **Não em todas as camadas.** Interpretador ≈ MVP OO ok; C/C++ **não**; sockets **não**. |
| **Fase do OO “completo” para demo** | **Interpretador: Fase 2 ✅** · **Fractal/recursão: Fase 3 ⬜** · **Sockets: Fase 3 ⬜** |
| **Fase do OO no compilador gcc** | **Fase 2.5** (refino opcional 3–6/jun) — **não** bloqueia se a demo OO usar Interpretador |
