## Cronograma

| Período | O que será feito | Responsável | Vertente | Diagramas (Mermaid) |
|---------|------------------|---------------|----------|---------------------|
| **29–30/mai** | Organizar o projeto: prioridades, board e mapa de reuso | **Bruno** | Projeto | `flowchart` — visão geral do pipeline (Frontend → Gateway → MS) |
| **29–30/mai** | Estrutura `.tex` base no Overleaf; cada um copia o projeto | **Bruno** (base) / **Todos** (cópia) | Documentação | — |
| **29–30/mai** | Diagrama de **arquitetura de microsserviços** (componentes + APIs) | **Bruno** | Projeto + LPS | `flowchart` ou `C4Context` — gateway, MS, PostgreSQL, frontend |
| **29/mai–02/jun** | `ms-front-end` (lexer + parser → AST JSON) | **Alan** | Compiladores | `flowchart` — fases léxica → sintática; opcional: árvore exemplo em `graph` |
| **30/mai–02/jun** | `ms-semantic` (tipos, escopo, tabela de símbolos) | **Karlisson** | Compiladores | `flowchart` — fluxo da análise semântica |
| **02/jun** | Integrar parser + semântica no gateway e validar na UI | **Bruno** | Projeto | `sequenceDiagram` — `POST /process` entre UI, gateway e MS |
| **02–04/jun** | Template Method + pacote compartilhado nos back-ends | **Karlisson** | Reuso | `classDiagram` — classe abstrata + variantes (Interpreter, C, Rust, ARM) |
| **03–05/jun** | `ms-interpreter` | **Karlisson** | Compiladores | — |
| **03–05/jun** | `ms-codegen-c` (C/C++ + `gcc -O2`) | **Alan** | Compiladores | `flowchart` — AST → C → gcc → executável |
| **04–05/jun** | Rust e ARM em nível MVP | **Alan** | Compiladores + LPS | — |
| **04–05/jun** | Pontos de variação e variantes (LPS) | **Maria** | LPS | Diagrama de **features** (árvore em `flowchart` ou tabela + figura); incluir no relatório |
| **05–07/jun** | `ms-parallel-coord` + teste 3 máquinas | **Alan** | Compiladores | `sequenceDiagram` — coordenador ↔ 3 workers via sockets |
| **06–07/jun** | Fractal (Sierpinski) + saída na UI | **Karlisson** | Compiladores | — (screenshot da matriz no cap. Resultados) |
| **06–07/jun** | Docker Compose + README | **Bruno** | Projeto | `flowchart` — serviços e portas do `docker-compose` |
| **07–08/jun** | Deploy (Vercel + gateway) e polimento da UI | **Bruno** | Projeto | `flowchart` — ambiente de produção (opcional, 1 diagrama simples) |
| **29/mai–05/jun** | Relatório: Introdução, Metodologia e Arquitetura | **Bruno** + **Maria** (Metodologia) | Documentação | Incluir diagramas de arquitetura e pipeline |
| **03–06/jun** | Relatório: BNF OO, AST e pipeline | **Alan** + **Karlisson** | Compiladores | BNF em texto/LaTeX; AST: `classDiagram` dos nós principais (`Program`, `ClassDecl`, `ParBlock`, etc.) |
| **04–06/jun** | Relatório: Reuso e Template Method | **Karlisson** + **Maria** (mapeamento) | Reuso | `flowchart` — origem (`cl-minipar` / `projeto_compiladores`) → componente do framework |
| **05–06/jun** | Relatório: LPS e variabilidade | **Maria** | LPS | Diagrama de features + `flowchart` de binding (variabilidade → MS escolhido) |
| **05–06/jun** | Relatório: UML | **Maria** | Documentação | `classDiagram`, `sequenceDiagram` (caso de uso “Compilar”), `flowchart` (componentes) |
| **07–08/jun** | Relatório: Resultados | **Maria** (material) + **Alan** / **Karlisson** (texto) | Documentação | Prints da UI + trechos dos diagramas acima |
| **08/jun** | Fechar PDF individual | **Todos** | Documentação | Revisar legenda e numeração de todas as figuras Mermaid |
| **07–08/jun** | Slides da apresentação | **Bruno** + **Maria** + **Alan** / **Karlisson** | Projeto | Reutilizar 4–6 diagramas Mermaid (arquitetura, LPS, pipeline, demo paralela) |
| **08–09/jun** | Roteiro e ensaio da demo | **Bruno** + **Alan** + **Karlisson** | Projeto | Slide com `sequenceDiagram` do fluxo ao vivo |
| **09/jun** | Ensaio geral + vídeo backup | **Todos** | Projeto | — |
| **10/jun** | Entrega | **Todos** | Entrega | — |

---

## Quem faz qual diagrama (resumo)

| Pessoa | Diagramas Mermaid principais |
|--------|----------------------------|
| **Bruno** | Arquitetura MS, pipeline E2E, sequência gateway, Docker/deploy |
| **Alan** | Fluxo léxico/sintático, codegen C/gcc, sequência 3 máquinas |
| **Karlisson** | Semântica, Template Method (`classDiagram`), AST (`classDiagram`) |
| **Maria** | Features LPS, UML (casos de uso, componentes, classes), mapa de reuso (com Karlisson) |

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

- **`minipar-framework/docs/diagrams/`** — arquivos `.mmd` no repo (Bruno cria a pasta no kick-off).
- **README** — 1 diagrama de arquitetura embutido.
- **Overleaf** — exportar SVG/PNG dos `.mmd` ou colar código se o template do professor permitir.