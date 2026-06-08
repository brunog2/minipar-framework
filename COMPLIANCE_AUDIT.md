# Auditoria de conformidade — MiniPar Framework 2026.1

**Propósito:** registrar o alinhamento do projeto com os requisitos das disciplinas (Compiladores, Reuso de Software, LPS/Tópicos) — o que está **conforme**, **parcial**, **não conforme** e **diferente do pedido** — para orientar implementações futuras, demo e entrega acadêmica.

**Referências:** [PROJECT_REQUIREMENTS.md](./PROJECT_REQUIREMENTS.md) · [ROADMAP.md](./ROADMAP.md) · [SCHEDULE.md](./SCHEDULE.md) · [ACTIVITIES.md](./ACTIVITIES.md) · [report.tex](./report.tex)  
**Última revisão:** 8 de junho de 2026  
**Entrega alvo:** 10 de junho de 2026

**Metodologia desta auditoria:** análise do repositório (`minipar-framework`), código, `docker-compose.yml`, microsserviços e documentação. Prioriza **o que está no código** quando há divergência com textos antigos de `ROADMAP`/`README`.

**Legenda:** ✅ conforme · 🟡 parcial / MVP / com ressalvas · ❌ não conforme · ➕ feito além ou diferente do pedido

---

## Resumo executivo

| Dimensão | Situação geral |
|----------|----------------|
| **Compiladores (pipeline OO)** | **Boa conformidade** — léxico → sintático → AST JSON → semântica (MVP) → back-ends |
| **Paralelismo “real” (requisito forte)** | **Parcial / risco alto** na avaliação estrita do professor |
| **Reuso + Template Method** | **Conforme** no núcleo e na documentação |
| **LPS / microsserviços** | **Conforme** na arquitetura; sem FeatureIDE (decisão do projeto) |
| **Testes obrigatórios (3 máq. + fractal)** | **Implementados com ressalvas** — validar E2E + evidências no PDF |
| **Entrega acadêmica** | **Bem encaminhado** — `report.tex` (~1168 linhas), 12 figuras PNG, extensão Python E2E, docs instanciação/banca |

**Veredito:** o projeto **cobre bem** o framework distribuído, OO no parse/execução e variabilidade LPS; **não está plenamente alinhado** com a leitura mais estrita de “`PAR` + processos independentes + sockets” e com “menu/programa MiniPar nas 3 máquinas”. Para a entrega de **10/jun**, o maior gap é **validação demonstrável** (E2E real + relatório com evidências), não só existência de código.

**Toolchains nos microsserviços (não no host):** `gcc`/`g++` em `ms-codegen-c`; `rustc` em `ms-codegen-rust` (Dockerfile). O desenvolvedor **não** precisa instalar Rust no laptop se usar `docker compose`.

---

## 1. Compiladores (MiniPar 2026.1 OO)

### ✅ Em conformidade

| Requisito | Evidência |
|-----------|-----------|
| **Gramática OO** (`class`, `extends`, `new`, atributos, métodos) | `parser.py`, `ast_nodes.py`, exemplos `01`–`09` |
| **Lexer** | `lexer.py` — tokens OO e paralelismo (`par`, `seq`, `s_channel`, `c_channel`) |
| **Parser descendente recursivo + AST** | `Parser` em `parser.py` |
| **AST serializável (JSON)** | `ast_json.py`, `_AST_CONTRACT.md`, REST entre MS |
| **Pipeline léxico → sintático → semântico → back-end** | `pipeline.service.ts`, `PIPELINE_MODE=http`, `PIPELINE_BACKEND_MODE=http` |
| **Microsserviços por fase/variante** | `ms-front-end`, `ms-semantic`, `ms-interpreter`, `ms-codegen-*` |
| **`gcc -O2` (C/C++)** | `c_backend.py`, `ms-codegen-c` |
| **Interpretador OO MVP** | `interpreter.py` — `new`, métodos, herança, `Main.run()`, `par`/`seq` locais |
| **Recursão (fractal)** | `13_sierpinski.minipar` com `this.isBlack(...)` recursivo |
| **BNF e pseudocódigos no relatório** | `report.tex` |

### 🟡 Parcialmente em conformidade

| Requisito | O que existe | Lacuna |
|-----------|--------------|--------|
| **Semântica + tabela de símbolos “completa”** | `semantic.py` + `symbol_table.py` | MS usa só **`semantic_json` MVP** (classes, `extends`, duplicatas) |
| **Codegen OO C/C++ alta performance** | TAC + `METHOD_CALL`/`NEW` em `c_codegen.py` | Validar E2E `09_oo_new` com **C** antes da banca |
| **Rust / ARM** | MS + backends MVP | Rust: `rustc` no container ✅; emissão ainda MVP (println). ARM: toolchain opcional |
| **Executável `.exe`** | Binário no container | Linux: `./program` — aceitar “executável nativo” |
| **Canais na linguagem** | Declaração `s_channel` / `c_channel` no parser | **`SendStmt` / `ReceiveStmt` não implementados** |
| **Verificação antes de compilar** | Parser + semântica | Enunciado cita “interpretador para sintaxe”; projeto usa **parser** (correto; documentar) |

### ❌ Não conforme (ou conforme só na demo alternativa)

| Requisito | Situação no código |
|-----------|-------------------|
| **`PAR` = processos independentes, sem memória compartilhada, só sockets** | `exec_par` usa **`threading` no mesmo processo** e `self.globals` compartilhado |
| **Paralelismo ligado à linguagem MiniPar no teste 3 máquinas** | Workers **Python** com algoritmos fixos (`parallel-workers/app/main.py`) |
| **Menu coordenador como programa MiniPar** | `14_distributed_menu.minipar` é placeholder; menu = **UI** + `ms-parallel-coord` |

---

## 2. Reuso de software

### ✅ Em conformidade

- Arquitetura por **componentes** (MS + `minipar-core`).
- **Template Method:** `AbstractBackendTranslator` — `validate → prepare → emit → finalize`.
- Variantes: `InterpreterBackend`, `CBackend`, `CppBackend`, `RustBackend`, `ARMBackend`, **`PythonBackend`** (extensão demo).
- Diagramas: `template-method.mmd`, `reuse-map.mmd`, `report.tex` (Gamma).
- **Reuso evolutivo 2025.1:** `code_references/cl-minipar`, `projeto_compiladores`.

### ✅ Atualizado (jun/2026)

- Figuras UML exportadas em `docs/figures/*.png` e referenciadas em `report.tex`.
- Extensão `PythonBackend` + `ms-codegen-python` + exemplo `16` + evidência E2E.
- Documentação de instanciação: `CREATING_AN_APPLICATION.md`, `applications/`, `BANCA_NARRATIVE.md`.

### ➕ Feito a mais (positivo)

- `translation/` unificado (TAC C/ARM).
- Modos `mock` no gateway para dev sem Docker.

---

## 3. LPS / microsserviços

### ✅ Em conformidade

| Requisito | Implementação |
|-----------|----------------|
| Pontos de variação e variantes | UI + gateway |
| Microsserviços REST + JSON | 7 MS + 3 workers |
| API Gateway | NestJS `POST /api/v1/process` |
| PostgreSQL | `compilation_history` |
| Docker Compose | Stack completa |
| Feature tree | `docs/diagrams/feature-tree.mmd` |

### ➕ Diferente do solicitado (documentar no relatório)

| Sugestão original | Implementação |
|-------------------|---------------|
| Gateway **Spring Boot** | **NestJS** (Node) |
| **FeatureIDE** | LPS por **microsserviços + UI** |
| Léxico e sintático em MS separados | **Unificados** em `ms-front-end` |

### 🟡 Pendente acadêmico

- Binding formal variante → MS no PDF.
- Vercel = só frontend; E2E pleno = **Docker local**.

---

## 4. Testes obrigatórios (professor)

### Teste 3 máquinas (QuickSort, matriz, fatorial)

| Aspecto | Status |
|---------|--------|
| 3 processos + sockets TCP | ✅ `ms-parallel-coord` + workers :9001–9003 |
| Coordenador agrega e exibe na UI | ✅ `DISTRIBUTED_SOCKETS`, `distributedResults` |
| 3 computadores físicos | 🟡 3 **containers** Docker |
| Algoritmos em MiniPar nos workers | ❌ Python fixo |
| Menu como programa MiniPar | ❌ Menu na UI |
| Disparo via blocos `PAR` | ❌ |

**Classificação:** 🟡 **parcialmente conforme** (infra); ❌ se exigirem MiniPar + `PAR` nos workers.

```bash
cd minipar-framework && docker compose up --build
curl -s -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"sourceCode":"class Main { void run() { println(\"ok\"); } }",
       "targetVariability":"INTERPRETER","executionMode":"DISTRIBUTED_SOCKETS"}'
```

Fixture: `14_distributed_menu.minipar`.

### Fractal (Tapete de Sierpinski)

| Aspecto | Status |
|---------|--------|
| Programa MiniPar OO recursivo | ✅ `13_sierpinski.minipar` |
| Matriz `.` / `*` no Console/UI | 🟡 confirmar E2E |
| Screenshot no relatório | ❌ |
| Testes automatizados | ❌ sem `pytest` no monorepo |

**Classificação:** 🟡 **provavelmente conforme** após `docker compose` + exemplo 13; ❌ evidência PDF.

---

## 5. Requisitos acadêmicos

### ✅ ou bem encaminhado

- Metodologia ágil: backlogs em `report.tex` + [ACTIVITIES.md](./ACTIVITIES.md).
- Pseudocódigos das fases e coordenador/worker.
- Referências: Pohl, Sommerville, Gamma, Maciel, Rego, spec 2026.
- Diagramas Mermaid versionados.
- Estrutura do relatório integrando 3 disciplinas.

### 🟡 / ❌ pendente

| Item | Situação |
|------|----------|
| UML no PDF | ✅ 12 figuras PNG em `docs/figures/` |
| Prints fractal + 3 máq. | ✅ figuras UI + sequência no PDF (`docs/figures/ui/`) |
| Extensão Python (demo framework) | ✅ `PythonBackend` + MS + registry + UI |
| Docs instanciação / banca | ✅ `CREATING_AN_APPLICATION.md`, `BANCA_NARRATIVE.md` |
| URL GitHub / vídeo | placeholders |
| Apresentação com todos os testes | ensaio ⬜ |

### ➕ Feito a mais

- Vercel, histórico Postgres, fixtures `01`–`16`, templates UI, `_template_backend.py`.

---

## 6. Matriz consolidada (checklist entrega 10/jun)

| Critério | Status |
|----------|--------|
| Pipeline MiniPar OO em microsserviços | ✅ |
| Template Method (C/Rust/ARM/Interpretador/Python) | ✅ |
| Variabilidade na UI + gateway | ✅ |
| Extensão Python (`PythonBackend` + MS :3008) | ✅ |
| Figuras UML/LPS no relatório (`docs/figures/*.png`) | ✅ |
| `gcc -O2` para C/C++ | ✅ |
| `rustc` no MS Rust (Docker) | ✅ |
| Interpretador OO para demo | ✅ MVP |
| Semântica “de compilador” no MS | 🟡 |
| Teste 3 máquinas via sockets | 🟡 |
| Fractal OO matriz de caracteres | 🟡 |
| `PAR` = processos + sockets | ❌ |
| Send/Receive na linguagem | ❌ |
| Relatório Overleaf + evidências | ✅ (diagramas + capturas UI) |
| GitHub + apresentação | 🟡 |

---

## 7. Pendências prioritárias (até 10/jun)

1. **Checklist E2E** — [ACTIVITIES.md](./ACTIVITIES.md#checklist-e2e-preencher-antes-da-banca) (inclui fixture `16_codegen_python`).
2. **Screenshots UI** opcionais → fractal e 3 máquinas (figuras de sequência já no PDF).
3. **Narrativa do paralelismo** na banca (3 containers = 3 PCs; workers Python) — ver [BANCA_NARRATIVE.md](./docs/BANCA_NARRATIVE.md).
4. **Validar** `09_oo_new` com **C** + `gcc -O2`.
5. **URLs** GitHub/vídeo finais no `report.tex`.
6. **Opcional pós-entrega:** `semantic.py` no MS; Send/Receive; `PAR` com sockets.

---

## 8. Feito diferente do pedido (documentar, não ocultar)

| Pedido / expectativa | Implementação |
|----------------------|----------------|
| Gateway Spring Boot | **NestJS** |
| FeatureIDE | LPS por microsserviços + feature tree |
| `PAR` → processos + sockets | `PAR` → **threads locais**; sockets no **teste dedicado** |
| Menu/programa MiniPar no PC1 | **Menu na UI Angular** |
| Workers executam MiniPar | Workers executam **Python fixo** |
| Interpretador para “checar sintaxe” | **Parser + semântica** |
| Três PCs físicos | **Três containers** |
| Toolchain no host | Toolchain **dentro do MS** (gcc, rustc) |
| Léxico e sintático em MS separados | **ms-front-end** unificado |

---

## 9. Documentação do projeto (sincronização)

| Documento | Papel |
|-----------|--------|
| **COMPLIANCE_AUDIT.md** (este) | Conformidade ✅/🟡/❌ |
| **SCHEDULE.md** | Datas e marcos |
| **ACTIVITIES.md** | Responsáveis, sprints, checklist E2E |
| **ROADMAP.md** | Entregas técnicas por fase |
| **PROJECT_REQUIREMENTS.md** | Especificação do professor |

Ao mudar código relevante, atualizar **este arquivo** e o checklist em **ACTIVITIES.md**.

---

## 10. Roteiro de demo (10/jun)

| # | Exemplo | Modo LPS |
|---|---------|----------|
| 1 | `08_interpreter_ok.minipar` | INTERPRETER + LOCAL |
| 2 | `09_oo_new.minipar` | INTERPRETER + LOCAL (`woof`) |
| 3 | `13_sierpinski.minipar` | INTERPRETER + LOCAL |
| 4 | `11_codegen_c.minipar` | C + LOCAL |
| 5 | qualquer fonte válida | INTERPRETER + **DISTRIBUTED_SOCKETS** |

**Não prometer:** `PAR` com sockets entre processos; QuickSort em MiniPar nos workers.

---

## 11. Referência rápida de artefatos

| Artefato | Caminho |
|----------|---------|
| Especificação | `PROJECT_REQUIREMENTS.md` |
| Cronograma | `SCHEDULE.md` |
| Atividades / E2E | `ACTIVITIES.md` |
| Fases técnicas | `ROADMAP.md` |
| Relatório | `report.tex` |
| Exemplos | `sources/examples/README.md` |
| Template Method | `packages/minipar-core/.../base_translator.py` |

---

## Histórico de revisões

| Data | Alteração |
|------|-----------|
| 2026-06-02 | Criação inicial — auditoria integrada |
| 2026-06-02 | Revisão completa alinhada ao código; `rustc` no MS Rust; docs SCHEDULE/ACTIVITIES; matriz e §8 explícitos |
| 2026-06-08 | Extensão Python E2E; 12 figuras PNG; `report.tex` (~1168 linhas) + apêndices; `applications/`; `GET /variants`; compliance sincronizado |
