# Auditoria de conformidade — MiniPar Framework 2026.1

**Propósito:** registrar o alinhamento do projeto com os requisitos das disciplinas (Compiladores, Reuso de Software, LPS/Tópicos) e orientar **implementações futuras**, demos e fechamento acadêmico.

**Referências:** [PROJECT_REQUIREMENTS.md](./PROJECT_REQUIREMENTS.md) · [ROADMAP.md](./ROADMAP.md) · [report.tex](./report.tex)  
**Última revisão:** 2 de junho de 2026  
**Entrega alvo:** 10 de junho de 2026

**Legenda:** ✅ conforme · 🟡 parcial / MVP / com ressalvas · ❌ não conforme · ➕ feito além ou diferente do pedido

---

## Resumo executivo

| Dimensão | Situação |
|----------|----------|
| Compiladores (pipeline OO) | Boa conformidade: léxico → sintático → AST JSON → semântica (MVP) → back-ends |
| Paralelismo “real” (requisito forte) | **Risco alto na banca:** `PAR` local ≠ sockets; teste 3 máquinas ≠ MiniPar nos workers |
| Reuso + Template Method | Conforme no código e diagramas |
| LPS / microsserviços | Conforme na arquitetura (sem FeatureIDE, por decisão) |
| Testes obrigatórios (3 máq. + fractal) | Infra implementada; validação E2E e evidências no PDF pendentes |
| Entrega acadêmica | Texto e `.mmd` avançados; screenshots, URLs finais e consistência docs pendentes |

**Veredito:** o framework atende bem LPS + pipeline + Template Method; **não está plenamente alinhado** com a leitura estrita de “`PAR` + processos independentes + sockets” nem com “programa/menu MiniPar nas três máquinas”. Priorizar **ensaio E2E** e **documentação honesta** na apresentação.

---

## 1. Compiladores (MiniPar 2026.1 OO)

### ✅ Em conformidade

| Requisito | Evidência no repositório |
|-----------|-------------------------|
| Gramática OO (`class`, `extends`, `new`, atributos, métodos) | `packages/minipar-core/minipar_core/parser.py`, `ast_nodes.py`, `sources/examples/01–09` |
| Análise léxica | `lexer.py` — tokens OO e `par` / `seq` / `s_channel` / `c_channel` |
| Parser descendente recursivo + AST | `parser.py` |
| AST serializável (JSON) entre microsserviços | `ast_json.py`, `microservices/_AST_CONTRACT.md` |
| Pipeline completo via HTTP | `api-gateway/src/pipeline/pipeline.service.ts` com `PIPELINE_MODE=http`, `PIPELINE_BACKEND_MODE=http` |
| `gcc -O2` (C/C++) | `translation/c_backend.py`, `ms-codegen-c` |
| Interpretador OO (MVP) | `translation/interpreter.py` — `new`, métodos, herança, `Main.run()`, `par`/`seq` locais |
| Fractal recursivo (fonte) | `sources/examples/13_sierpinski.minipar` |
| BNF e pseudocódigos (relatório) | `report.tex` § Fases do compilador |

### 🟡 Parcialmente em conformidade

| Requisito | O que existe | Lacuna / ação futura |
|-----------|--------------|----------------------|
| Análise semântica + tabela de símbolos “completa” | `semantic.py` + `symbol_table.py` no pacote | **`ms-semantic` usa apenas `semantic_json.py` (MVP).** Migrar MS para `SemanticAnalyzer` + `analyze_program` quando fractal/OO avançado exigir tipos e escopo ricos |
| Codegen OO em C/C++ | TAC + `METHOD_CALL` / `NEW` em `c_codegen.py` | Validar E2E `09_oo_new.minipar` com `targetVariability: C`; não prometer na demo sem teste |
| Rust / ARM | `ms-codegen-rust`, `ms-codegen-arm` | MVP: emissão de código; `rustc`/toolchain ARM opcionais no container |
| Executável `.exe` | Binário nativo no container | Em Linux gera `./program`; documentar como “executável nativo” |
| Canais na linguagem | `channel_declaration()` no parser | **`SendStmt` / `ReceiveStmt` não implementados** (só no contrato AST) |
| “Interpretador para verificação sintática” antes de compilar | Parser + semântica no pipeline | Abordagem correta; **diferente do texto do enunciado** — justificar no relatório |

### ❌ Não conforme (ou só conforme via demo alternativa)

| Requisito | Situação atual | Implementação futura sugerida |
|-----------|----------------|------------------------------|
| `PAR` com threads como **processos independentes**, **sem memória compartilhada**, comunicação **só por sockets** | `exec_par` usa `threading` no **mesmo processo** e compartilha `self.globals` | Opção mínima: documentar limitação. Opção forte: runtime que dispare subprocessos/workers por ramo `par` + protocolo socket |
| Paralelismo ligado à **linguagem MiniPar** no teste 3 máquinas | Workers Python com algoritmos fixos (`microservices/parallel-workers/`) | Opcional: compilar/interpretar `quicksort.minipar` etc. em cada worker |
| Menu coordenador como **programa MiniPar** | `14_distributed_menu.minipar` é placeholder; menu real = **UI Angular** | Opcional: programa MiniPar que use canais/sockets quando parser suportar |

---

## 2. Reuso de software

### ✅ Em conformidade

- Componentes por fase/variante encapsulados em microsserviços FastAPI + núcleo `minipar-core`.
- **Template Method:** `AbstractBackendTranslator` (`translation/base_translator.py`) — `validate → prepare → emit → finalize`.
- Hotspots: `InterpreterBackend`, `CBackend`, `CppBackend`, `RustBackend`, `ARMBackend`.
- Reuso 2025.1 documentado: `code_references/cl-minipar`, `code_references/projeto_compiladores` → `docs/diagrams/reuse-map.mmd`, `report.tex`.

### 🟡 Parcial

- Prova acadêmica no PDF: exportar diagramas `.mmd` para figuras no Overleaf (UML por componente).

### ➕ Além do pedido

- Módulo `translation/` unificado (TAC compartilhado C/ARM).
- Modos `mock` no gateway para desenvolvimento sem stack completa.

---

## 3. LPS / microsserviços

### ✅ Em conformidade

| Requisito | Implementação |
|-----------|----------------|
| Pontos de variação e variantes | UI: interpretador vs compilador; C/C++/Rust/ARM; LOCAL vs `DISTRIBUTED_SOCKETS` |
| Microsserviços REST + JSON | `ms-front-end` … `ms-codegen-arm`, `ms-parallel-coord` |
| API Gateway orquestrador | NestJS `POST /api/v1/process` |
| PostgreSQL | `database/init.sql` → `compilation_history` |
| Docker Compose | `docker-compose.yml` (inclui workers :9001–9003) |
| Diagrama de features | `docs/diagrams/feature-tree.mmd` |

### ➕ Diferente do sugerido (documentar, não ocultar)

| Sugestão original | Escolha do projeto |
|-------------------|-------------------|
| API Gateway Spring Boot | **NestJS** (Node.js) |
| FeatureIDE | Variabilidade **arquitetural** (MS + UI) |
| Léxico e sintático em MS separados | **Unificados** em `ms-front-end` |

### 🟡 Pendente acadêmico

- Binding formal variante → microsserviço no PDF final.
- Demo Vercel: frontend sem stack completa — deixar claro que E2E pleno é **Docker local**.

---

## 4. Testes obrigatórios (professor)

### Teste 3 máquinas (QuickSort, matriz, fatorial)

| Aspecto | Status | Notas |
|---------|--------|-------|
| 3 processos + sockets TCP | ✅ | `ms-parallel-coord` + `worker-quicksort` / `worker-matrix` / `worker-factorial` |
| Agregação na UI | ✅ | `DISTRIBUTED_SOCKETS` + `distributedResults` no gateway/UI |
| 3 PCs físicos | 🟡 | 3 **containers** na rede Docker — aceitável se explicado na banca |
| Algoritmos em MiniPar nos workers | ❌ | Lógica em Python nos workers |
| Menu MiniPar no PC1 | ❌ | Menu na UI |
| Disparo via `PAR` da linguagem | ❌ | Não conectado ao coordenador |

**Como testar:**

```bash
cd minipar-framework && docker compose up --build
curl -s -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"sourceCode":"class Main { void run() { println(\"ok\"); } }",
       "targetVariability":"INTERPRETER","executionMode":"DISTRIBUTED_SOCKETS"}'
```

`pipelineSteps` esperado (com backend http): `ms-front-end: parse`, `ms-semantic: analyze`, `ms-parallel-coord: coordinate`, `ms-interpreter: execute`.

Fixture: `sources/examples/14_distributed_menu.minipar`.

### Fractal (Tapete de Sierpinski)

| Aspecto | Status | Notas |
|---------|--------|-------|
| Programa MiniPar OO recursivo | ✅ | `sources/examples/13_sierpinski.minipar` |
| Matriz `.` / `*` no Console | 🟡 | Via `println` + interpretador; **confirmar E2E** |
| Screenshots no relatório | ❌ | Incluir `\includegraphics` no `report.tex` após ensaio |

**Como testar:** UI → exemplo Sierpinski → **INTERPRETER** + **LOCAL** → Executar.

---

## 5. Requisitos acadêmicos

### ✅ / 🟡

| Item | Status |
|------|--------|
| Metodologia ágil (backlogs) | ✅ `report.tex` |
| Pseudocódigos das fases | ✅ `report.tex` |
| Referências (Pohl, Sommerville, Gamma, Maciel, Rego, spec 2026) | ✅ bibliografia |
| Diagramas Mermaid | ✅ `docs/diagrams/` |
| UML no PDF | 🟡 exportar `.mmd` → figuras |
| Prints fractal + 3 máquinas | ❌ pendente |
| URL GitHub / vídeo finais | ❌ placeholders em `report.tex` |
| Consistência ROADMAP/README vs código | ❌ ver § 6 |

---

## 6. Inconsistências internas (manter sincronizado)

Ao alterar implementação, atualizar **este arquivo** e o [ROADMAP.md](./ROADMAP.md).

| Documento | Problema |
|-----------|----------|
| `ROADMAP.md` | Mapa ainda marca Fase 3 (paralelismo/fractal) como ⬜ em trechos; panorama diz ✅ |
| `README.md` | Lista `ms-parallel-coord` como pendente; exemplos só até `12` |
| `report.tex` | Afirma Fase 3 concluída; falta evidência visual |
| `docs/diagrams/README.md` | Pode listar `ms-parallel-coord` como pendente |
| `pipeline.service.ts` | Caminho `mock` com resultados hardcoded (ok para dev; Docker usa `http`) |

---

## 7. Matriz consolidada (checklist entrega)

| Critério | Status |
|----------|--------|
| Pipeline MiniPar OO em microsserviços | ✅ |
| Template Method (C/Rust/ARM/Interpretador) | ✅ |
| Variabilidade na UI + gateway | ✅ |
| `gcc -O2` para C/C++ | ✅ |
| Interpretador OO para demo | ✅ MVP |
| Semântica “de compilador” no MS | 🟡 |
| Teste 3 máquinas via sockets | 🟡 infra OK; sem MiniPar `PAR` |
| Fractal OO matriz de caracteres | 🟡 código OK; validar + print PDF |
| `PAR` = processos + sockets | ❌ |
| Send/Receive na linguagem | ❌ |
| Relatório Overleaf completo | 🟡 |
| GitHub + apresentação ao vivo | 🟡 |

---

## 8. Backlog para implementações futuras

Prioridade sugerida **após** fechar entrega 10/jun (ou se sobrar tempo antes):

### P0 — Entrega / banca (não código)

1. Ensaiar E2E Docker: exemplos `13`, `14`, `09` (C), `08`.
2. Screenshots → `report.tex` (fractal + menu distribuído + pipeline steps).
3. URLs finais GitHub e vídeo; alinhar `ROADMAP.md` e `README.md` com este documento.

### P1 — Conformidade semântica

4. `ms-semantic` passar a usar `semantic.py` / `analyze_program` (ou híbrido: MVP + erros do analisador completo).
5. Testes automatizados mínimos (`pytest`) para parse, semântica e interpretador nos exemplos `01–14`.

### P2 — Paralelismo (se professor exigir literalidade)

6. Parser: `SendStmt` / `ReceiveStmt` (ver `_AST_CONTRACT.md` e `code_references/projeto_compiladores/examples/`).
7. Runtime interpretador: canais TCP alinhados a `s_channel` / `c_channel`.
8. Opcional: `exec_par` via subprocessos + sockets em vez de threads com memória compartilhada.
9. Opcional: workers executando bytecode/AST MiniPar em vez de Python fixo.

### P3 — Codegen OO

10. Fechar OO no `gcc` (`new`, `d.bark()`, herança) com testes em `09_oo_new.minipar` + C.
11. Despacho dinâmico / `super` no codegen C (hoje mais forte no interpretador).

### P4 — Acadêmico / LPS

12. Figuras UML e feature tree embutidas no PDF.
13. Seção “decisões arquiteturais” (NestJS, parser vs interpretador para sintaxe, 3 containers vs 3 PCs).

---

## 9. Roteiro de demo recomendado (10/jun)

| # | Exemplo | Modo LPS | O que mostrar |
|---|---------|----------|----------------|
| 1 | `08_interpreter_ok.minipar` | INTERPRETER + LOCAL | Pipeline real, saída `ok` |
| 2 | `09_oo_new.minipar` | INTERPRETER + LOCAL | `new` + método → `woof` |
| 3 | `13_sierpinski.minipar` | INTERPRETER + LOCAL | Matriz 27×27 `.`/`*` |
| 4 | `11_codegen_c.minipar` | C + LOCAL | `gcc -O2` + código gerado |
| 5 | qualquer fonte válida | INTERPRETER + **DISTRIBUTED_SOCKETS** | PC1–PC3, `distributedResults`, steps com `ms-parallel-coord` |

**Evitar prometer na fala (salvo implementar antes):** `PAR` com sockets entre processos; QuickSort em MiniPar nos workers.

---

## 10. Referência rápida de artefatos

| Artefato | Caminho |
|----------|---------|
| Especificação integrada | `PROJECT_REQUIREMENTS.md` |
| Cronograma e fases | `ROADMAP.md`, `SCHEDULE.md` |
| Relatório Overleaf | `report.tex` |
| Contrato AST | `microservices/_AST_CONTRACT.md` |
| Exemplos de validação | `sources/examples/README.md` |
| Coordenador distribuído | `microservices/ms-parallel-coord/` |
| Workers socket | `microservices/parallel-workers/` |
| Template Method | `packages/minipar-core/minipar_core/translation/base_translator.py` |

---

## Histórico de revisões

| Data | Alteração |
|------|-----------|
| 2026-06-02 | Criação inicial — auditoria integrada Compiladores + Reuso + LPS + acadêmico |
