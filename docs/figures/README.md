# Figuras exportadas — MiniPar Framework

PNG gerados a partir dos diagramas Mermaid em [`../diagrams/`](../diagrams/) para inclusão no relatório LaTeX (`report.tex`).

**Comando de exportação:**

```bash
npx @mermaid-js/mermaid-cli -i docs/diagrams/<nome>.mmd -o docs/figures/<nome>.png -b white -w 1200
```

## Índice de figuras

| Arquivo PNG | Diagrama fonte | Seção do relatório |
|-------------|----------------|-------------------|
| [architecture.png](./architecture.png) | `architecture.mmd` | Parte II (Framework), Parte V (LPS) |
| [template-method.png](./template-method.png) | `template-method.mmd` | Parte II, Parte IV (Reuso) |
| [uml-classes-framework.png](./uml-classes-framework.png) | `uml-classes-framework.mmd` | Parte II, Parte III (Compiladores) |
| [uml-use-cases.png](./uml-use-cases.png) | `uml-use-cases.mmd` | Parte I (Introdução) |
| [uml-components.png](./uml-components.png) | `uml-components.mmd` | Parte V (LPS) |
| [feature-tree.png](./feature-tree.png) | `feature-tree.mmd` | Parte V (LPS) |
| [pipeline-sequence.png](./pipeline-sequence.png) | `pipeline-sequence.mmd` | Parte II, Parte V, Parte VII |
| [frontend-semantic-flow.png](./frontend-semantic-flow.png) | `frontend-semantic-flow.mmd` | Parte III (Compiladores) |
| [codegen-c-flow.png](./codegen-c-flow.png) | `codegen-c-flow.mmd` | Parte III (Compiladores) |
| [reuse-map.png](./reuse-map.png) | `reuse-map.mmd` | Parte IV (Reuso) |
| [sequence-3-machines.png](./sequence-3-machines.png) | `sequence-3-machines.mmd` | Parte VII (Testes) |
| [validation-cases.png](./validation-cases.png) | `validation-cases.mmd` | Parte VII (Testes) |

**Total:** 12 diagramas (todos os `.mmd` em `docs/diagrams/`).

## Capturas de tela da UI (`ui/`)

Geradas com Playwright (`scripts/capture-ui-screenshots.mjs`). Requer `ng serve` na porta 4201 e stack Docker (`docker compose up`).

| Arquivo PNG | Conteúdo | Seção do relatório |
|-------------|----------|-------------------|
| [ui/01-pipeline-codegen-c.png](./ui/01-pipeline-codegen-c.png) | Pipeline C + gcc | Parte VII — Fig. pipeline |
| [ui/02-fractal-sierpinski.png](./ui/02-fractal-sierpinski.png) | Fractal no Console | Parte VII — Fig. fractal |
| [ui/03-python-extension.png](./ui/03-python-extension.png) | Extensão Python | Parte VII — Fig. Python |
| [ui/04-lps-feature-panel.png](./ui/04-lps-feature-panel.png) | Painel LPS | Parte VII — Fig. variabilidade |

```bash
cd minipar-framework/frontend && npm start -- --port 4201
cd minipar-framework && node scripts/capture-ui-screenshots.mjs
```

## Uso no LaTeX

```latex
\graphicspath{{docs/figures/}}
\includegraphics[width=0.9\textwidth]{architecture.png}
```

## Regeneração

```bash
cd minipar-framework
for f in docs/diagrams/*.mmd; do
  name=$(basename "$f" .mmd)
  npx @mermaid-js/mermaid-cli -i "$f" -o "docs/figures/${name}.png" -b white -w 1200
done
```
