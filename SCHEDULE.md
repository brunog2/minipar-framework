## Cronograma

Legenda: `[x] ok (Nome)` = concluído · `[ ]` = pendente · `[~]` = em andamento / parcial

---

### 29–30/mai — Kick-off

- [x] ok (Bruno) Organizar o projeto: prioridades, board e mapa de reuso — `flowchart` visão geral do pipeline (Frontend → Gateway → MS)
- [x] ok (Bruno) Estrutura `.tex` base no Overleaf (`report.tex`)
- [ ] Cada um copia o projeto (Todos)
- [x] ok (Bruno) Diagrama de **arquitetura de microsserviços** (componentes + APIs) — `docs/diagrams/architecture.mmd`

---

### 29/mai–02/jun — Análise (Compiladores)

- [ ] `ms-front-end` (lexer + parser → AST JSON) — **Alan** — `flowchart` fases léxica → sintática
- [ ] `ms-semantic` (tipos, escopo, tabela de símbolos) — **Karlisson** — `flowchart` fluxo da análise semântica
  - ⚠️ *Depende de:* `ms-front-end` (AST JSON)

---

### 02/jun — Integração

- [~] (Bruno) Integrar parser + semântica no gateway e validar na UI — `sequenceDiagram` `POST /process`
  - ok (Bruno): gateway (`api-gateway`), UI Angular, pipeline mock + HTTP, `docs/diagrams/pipeline-sequence.mmd`
  - pendente: MS reais de Alan e Karlisson para `PIPELINE_MODE=http`
  - ⚠️ *Depende de:* `ms-front-end`, `ms-semantic`

---

### 02–04/jun — Reuso

- [ ] Template Method + pacote compartilhado nos back-ends — **Karlisson** — `classDiagram` abstrata + variantes
  - ⚠️ *Depende de:* contrato AST / semântica definidos

---

### 03–05/jun — Back-ends (Compiladores)

- [ ] `ms-interpreter` — **Karlisson**
- [ ] `ms-codegen-c` (C/C++ + `gcc -O2`) — **Alan** — `flowchart` AST → C → gcc → executável
  - ⚠️ *Depende de:* Template Method, `ms-semantic`
- [ ] Rust e ARM em nível MVP — **Alan**
  - ⚠️ *Depende de:* `ms-codegen-c` (padrão de codegen)
- [ ] Pontos de variação e variantes (LPS) — **Maria** — diagrama de features
  - ⚠️ *Depende de:* arquitetura LPS documentada (base ok em `architecture.mmd`)

---

### 05–07/jun — Paralelismo e infra

- [ ] `ms-parallel-coord` + teste 3 máquinas — **Alan** — `sequenceDiagram` coordenador ↔ 3 workers
  - ⚠️ *Depende de:* pipeline de análise + back-end funcional
- [ ] Fractal (Sierpinski) + saída na UI — **Karlisson**
  - ⚠️ *Depende de:* `ms-interpreter` funcional
- [x] ok (Bruno) Docker Compose + README — `docker-compose.yml`, stack Postgres + Gateway + Frontend
  - diagrama de serviços/portas incluído em `architecture.mmd`

---

### 07–08/jun — Deploy e polimento

- [~] (Bruno) Deploy (Vercel + gateway) e polimento da UI
  - ok (Bruno): frontend em produção — [minipar-framework.vercel.app](https://minipar-framework.vercel.app/)
  - pendente: gateway em ambiente de produção / polimento final da UI

---

### 29/mai–05/jun — Relatório (parte 1)

- [~] (Bruno) + **Maria** (Metodologia) — Introdução, Metodologia e Arquitetura
  - ok (Bruno): esqueleto LaTeX + diagramas de arquitetura e pipeline
  - pendente: texto final das seções + Metodologia (Maria)

---

### 03–06/jun — Relatório (Compiladores)

- [ ] BNF OO, AST e pipeline — **Alan** + **Karlisson**
  - ⚠️ *Depende de:* `ms-front-end`, `ms-semantic` implementados

---

### 04–06/jun — Relatório (Reuso)

- [ ] Reuso e Template Method — **Karlisson** + **Maria** (mapeamento)
  - ⚠️ *Depende de:* Template Method implementado

---

### 05–06/jun — Relatório (LPS e UML)

- [ ] LPS e variabilidade — **Maria**
- [ ] UML — **Maria**

---

### 07–08/jun — Relatório (Resultados) e apresentação

- [ ] Resultados — **Maria** (material) + **Alan** / **Karlisson** (texto)
  - ⚠️ *Depende de:* testes paralelos, fractal e demo funcionando
- [ ] Fechar PDF individual — **Todos**
- [ ] Slides da apresentação — **Bruno** + **Maria** + **Alan** / **Karlisson**
  - ⚠️ *Depende de:* relatório e diagramas finalizados

---

### 08–09/jun — Demo

- [ ] Roteiro e ensaio da demo — **Bruno** + **Alan** + **Karlisson**
  - ⚠️ *Depende de:* pipeline E2E com MS reais

---

### 09–10/jun — Entrega

- [ ] Ensaio geral + vídeo backup — **Todos**
- [ ] Entrega — **Todos**

---

## Dependências entre demandas (resumo)

| Demanda | Depende de |
|---------|------------|
| `ms-semantic` (Karlisson) | `ms-front-end` (AST JSON) |
| Integração gateway + UI real (Bruno) | `ms-front-end` + `ms-semantic` |
| Template Method (Karlisson) | contrato AST / semântica |
| `ms-interpreter`, `ms-codegen-c` | semântica + Template Method |
| Rust / ARM MVP (Alan) | padrão estabelecido em `ms-codegen-c` |
| `ms-parallel-coord` | pipeline de análise + execução |
| Fractal na UI (Karlisson) | `ms-interpreter` |
| Relatório BNF/AST (Alan + Karlisson) | MS de front-end e semântica |
| Relatório Reuso (Karlisson + Maria) | Template Method implementado |
| Relatório Resultados | paralelismo + fractal + demo |
| Slides / roteiro demo | sistema funcional + relatório |
| PDF final / entrega | todas as seções acima |

**Caminho crítico:** kick-off (Bruno) → `ms-front-end` (Alan) → `ms-semantic` (Karlisson) → integração gateway (Bruno) → Template Method (Karlisson) → back-ends → paralelismo/fractal → resultados → entrega.

---

## Quem faz qual diagrama (resumo)

| Pessoa | Diagramas Mermaid principais | Status |
|--------|----------------------------|--------|
| **Bruno** | Arquitetura MS, pipeline E2E, sequência gateway, Docker/deploy | ok (Bruno): `architecture.mmd`, `pipeline-sequence.mmd` |
| **Alan** | Fluxo léxico/sintático, codegen C/gcc, sequência 3 máquinas | pendente |
| **Karlisson** | Semântica, Template Method (`classDiagram`), AST (`classDiagram`) | pendente |
| **Maria** | Features LPS, UML (casos de uso, componentes, classes), mapa de reuso (com Karlisson) | pendente |

---

## Tipos Mermaid por vertente

| Vertente | Sugestão Mermaid |
|----------|------------------|
| **Projeto** | `flowchart LR`, `sequenceDiagram` |
| **Compiladores** | `flowchart TD`, `classDiagram` (AST) |
| **Reuso** | `flowchart` (origem → componente), `classDiagram` (Template Method) |
| **LPS** | `flowchart` (feature tree / variante → MS) |
| **Documentação** | Exportar PNG/SVG (Mermaid Live, VS Code, ou `\usepackage{mermaid}` no Overleaf se disponível) |

---

## Onde versionar

- **`minipar-framework/docs/diagrams/`** — arquivos `.mmd` no repo — ok (Bruno): pasta criada
- **README** — 1 diagrama de arquitetura embutido — ok (Bruno): link para `docs/diagrams/`
- **Overleaf** — exportar SVG/PNG dos `.mmd` ou colar código se o template do professor permitir
