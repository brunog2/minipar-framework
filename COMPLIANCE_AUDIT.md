# Auditoria de conformidade — MiniPar Framework 2026.1

**Propósito:** registrar o alinhamento do projeto com os requisitos das disciplinas (Compiladores, Reuso de Software, LPS/Tópicos) — o que está **conforme**, **parcial**, **não conforme** e **diferente do pedido**.

**Referências:** [PROJECT_REQUIREMENTS.md](./PROJECT_REQUIREMENTS.md) · [ROADMAP.md](./ROADMAP.md) · [ACTIVITIES.md](./ACTIVITIES.md) · [report.tex](./report.tex) · [report.md](./report.md)  
**Última revisão:** 8 de junho de 2026 (pós `validate-all.sh` **15/15 PASS**)  
**Evidência automatizada:** [`docs/evidence/validation-results.json`](./docs/evidence/validation-results.json) · guia [`docs/VALIDATION.md`](./docs/VALIDATION.md)

**Legenda:** ✅ conforme · 🟡 parcial / MVP / ressalva · ❌ não conforme · ➕ feito além ou diferente do pedido (documentado)

**Metodologia:** análise do código + execução de `./scripts/validate-all.sh` com `docker compose up`. Prioriza **o que está no código e nos testes** sobre textos antigos de roadmap.

---

## Resumo executivo

| Dimensão | Situação | Nota |
|----------|----------|------|
| **Compiladores (pipeline OO)** | ✅ **Conforme** | E1, E2, E5, E6, E7, E8, E12 validados |
| **Paralelismo + canais** | ✅ **Conforme** | E4, E10, E11 — processos + broker TCP + workers MiniPar |
| **Testes obrigatórios (professor)** | ✅ **Conforme** | Fractal E3; 3 máquinas E4/E10 (containers 🟡) |
| **Reuso + Template Method** | ✅ **Conforme** | 6 back-ends + extensão Python |
| **LPS / microsserviços** | ✅ **Conforme** | REST, gateway, variantes, recomendações |
| **Entrega acadêmica** | 🟡 **Quase completa** | `report.pdf` (40 pág.) gerado; vídeo ⬜ |

**Veredito:** o projeto **atende** aos requisitos técnicos centrais do professor (pipeline OO, paralelismo real via sockets, fractal, back-ends com toolchain no MS, framework Arturo). Pendências restantes são **operacionais** (PDF final, vídeo, ensaio banca) e **MVPs opcionais** (tipagem semântica plena, ARM, CI pytest).

---

## Validação automatizada (8/jun/2026)

Comando: `docker compose up -d && ./scripts/validate-all.sh` → **15/15 PASS**

| ID | Caso | Variante / modo | Critério | Status |
|----|------|-----------------|----------|--------|
| GW | Gateway health | — | HTTP 200 | ✅ |
| E1 | `08_interpreter_ok` | INTERPRETER · LOCAL | saída `ok` | ✅ |
| E7 | `05_parse_extends_missing` | INTERPRETER · LOCAL | erro de **parser** | ✅ |
| E2 | `09_oo_new` | local core | `woof` | ✅ |
| E6 | `12_codegen_rust_stub` | RUST · LOCAL | `rustc` + stdout | ✅ |
| E3 | `13_sierpinski` | INTERPRETER · LOCAL | matriz fractal | ✅ |
| E4 | `08` | DISTRIBUTED_SOCKETS | PC1–PC3 (coord legado) | ✅ |
| E10 | `14_distributed_menu` | DISTRIBUTED_SOCKETS | menu MiniPar + IP:porta | ✅ |
| E8 | `04_semantic_extends_unknown` | INTERPRETER · LOCAL | erro **semântico** | ✅ |
| E5 | `11_codegen_c` | local core | `gcc -O2` | ✅ |
| E12 | `09_oo_new` | C · local core | `woof` + gcc | ✅ |
| E9 | `16_codegen_python` | PYTHON · LOCAL | extensão Python | ✅ |
| E11 | `15_channels` | local core | canais socket → `42` | ✅ |
| — | `GET /variants` | — | lista LPS | ✅ |
| — | `GET /recommendations` | — | histórico PG | ✅ |

---

## 1. Compiladores (MiniPar 2026.1 OO)

### ✅ Conforme

| Requisito | Evidência | Validação |
|-----------|-----------|-----------|
| Gramática OO (`class`, `extends`, `new`, métodos, atributos) | `parser.py`, exemplos `01`–`09` | E2 |
| Lexer + tokens de paralelismo | `lexer.py` — `par`, `seq`, `s_channel`, `c_channel` | E11 |
| Parser descendente recursivo + AST JSON | `parser.py`, `_AST_CONTRACT.md` | pipeline HTTP |
| Pipeline léxico → sintático → semântico → back-end | `pipeline.service.ts` | E1, E8 |
| Erro sintático antes de executar | `ms-front-end` | **E7** |
| Erro semântico | `semantic_full.py` → `SemanticAnalyzer` | **E8** |
| `gcc -O2` (C/C++) | `c_backend.py`, `ms-codegen-c` | E5, E12 |
| `rustc -O` (Rust) | `rust_backend.py`, `ms-codegen-rust` | **E6** |
| Interpretador OO | `interpreter.py` | E1, E2, E3 |
| Recursão / fractal | `13_sierpinski.minipar` | **E3** |
| `PAR` + IPC socket | `exec_par` + `ChannelBroker` | E11 |
| `send` / `receive` | `interpreter.py`, `socket_channel.py` | E11 |
| BNF e pseudocódigos no relatório | `report.tex`, `report.md` | docs |

### 🟡 Parcial

| Requisito | O que existe | Lacuna |
|-----------|--------------|--------|
| **Semântica “completa”** | Classes, `extends`, canais, escopo `par`/receive | Tipagem dinâmica; sem verificação rigorosa de tipos |
| **Codegen OO C/Rust** | OO em C (E12) e Rust stub (E6) | Rust/ARM: emissão MVP (println); sem `minipar_rt` em Rust |
| **Back-end ARM** | `ms-codegen-arm`, TAC → ARMv7 | Toolchain opcional; sem teste E2E no `validate-all` |
| **Executável `.exe`** | Binário nativo no container Linux | Não gera `.exe` Windows; aceitar binário ELF como “executável” |
| **3 PCs físicos** | 3 containers Docker + sockets TCP | Topologia lógica equivalente; não são máquinas separadas |

### ❌ Não conforme (baixo impacto na banca)

| Requisito | Situação |
|-----------|----------|
| **Testes automatizados no CI** | Sem `pytest` / GitHub Actions para regressão |
| **Hotspots lexer/parser alternativos** | Apenas implementação manual (roadmap) |

---

## 2. Reuso de software

### ✅ Conforme

| Requisito | Evidência |
|-----------|-----------|
| Arquitetura por componentes (MS + `minipar-core`) | `docker-compose.yml`, 8 MS + workers |
| **Template Method** | `AbstractBackendTranslator` — `validate → prepare → emit → finalize` |
| Hotspots por variante | `c_backend.py`, `interpreter.py`, `rust_backend.py`, `python_backend.py`, … |
| Reuso 2025.1 | `code_references/cl-minipar`, `projeto_compiladores` |
| Extensão sem alterar frozen-spots | `PythonBackend` + `ms-codegen-python` — **E9** |
| Documentação de instanciação | `CREATING_AN_APPLICATION.md`, `applications/`, `BANCA_NARRATIVE.md` |

### 🟡 Parcial

| Item | Situação |
|------|----------|
| Métricas formais de reuso (% LOC) | Não calculadas no relatório |

---

## 3. LPS / microsserviços

### ✅ Conforme

| Requisito | Evidência | Validação |
|-----------|-----------|-----------|
| Microsserviços REST + JSON | 8 MS + 3 workers | GW |
| API Gateway central | NestJS `POST /api/v1/process` | E1–E10 |
| Pontos de variação e variantes | UI + `backend-registry.ts` | GET variants |
| Binding runtime | `targetVariability`, `executionMode` | casos E2E |
| PostgreSQL / histórico | `compilation_history` | GET recommendations |
| Docker Compose | Stack completa | `docker compose` |
| Feature tree documentada | `docs/diagrams/feature-tree.mmd` | `report.tex` |

### ➕ Diferente do solicitado (aceito e documentado)

| Pedido original | Implementação |
|-----------------|---------------|
| Gateway **Spring Boot** | **NestJS** (Node) |
| **FeatureIDE** | LPS por microsserviços + feature tree + registry |
| Léxico e sintático em MS separados | Unificados em `ms-front-end` |

### 🟡 Parcial

| Item | Situação |
|------|----------|
| Vercel (UI demo) | Frontend estático; E2E pleno exige Docker local |
| Binding formal variante→MS no PDF | Descrito em texto; sem FeatureIDE |

---

## 4. Testes obrigatórios (professor)

### 4.1 Paralelismo em 3 máquinas

| Aspecto | Status | Evidência |
|---------|--------|-----------|
| QuickSort, matriz, fatorial | ✅ | Workers `worker_*.minipar` |
| Comunicação via sockets | ✅ | `c_channel` + TCP :9001–9003 |
| Resultados no coordenador/UI | ✅ | **E4** (legado), **E10** (menu MiniPar) |
| Menu como programa MiniPar | ✅ | `14_distributed_menu.minipar` |
| Identificação IP:porta | ✅ | saída E10 com host:porta |
| 3 computadores físicos | 🟡 | 3 **containers** Docker |

**Classificação:** ✅ **conforme** (ressalva: containers em vez de PCs físicos).

### 4.2 Fractal Sierpinski

| Aspecto | Status | Evidência |
|---------|--------|-----------|
| MiniPar OO recursivo | ✅ | `13_sierpinski.minipar` |
| Matriz `.` / `*` | ✅ | **E3** — 27×27 |
| Screenshot no relatório | ✅ | `docs/figures/ui/02-fractal-sierpinski.png` |

**Classificação:** ✅ **conforme**.

---

## 5. Requisitos acadêmicos

### ✅ Conforme ou entregue

| Item | Evidência |
|------|-----------|
| Metodologia ágil / backlogs | `report.tex`, `ACTIVITIES.md` |
| Relatório integrado 3 disciplinas | `report.tex` + `report.md` |
| Diagramas UML/LPS | 12+ figuras em `docs/figures/` |
| Pseudocódigos fases + coordenador/worker | `report.tex` §3 |
| Extensão Python (demo framework) | E9 |
| Docs instanciação / banca | `CREATING_AN_APPLICATION.md`, `BANCA_NARRATIVE.md` |
| URL GitHub | `https://github.com/brunog2/minipar-framework` |

### 🟡 Pendente operacional

| Item | Situação |
|------|----------|
| PDF Overleaf final | `./scripts/package-overleaf.sh` — upload manual |
| URL vídeo apresentação | Placeholder no `report.tex` |
| Ensaio oral banca | `docs/BANCA_NARRATIVE.md` — não realizado |
| Checklist assinado pela equipe | Automatizado 15/15; assinatura manual ⬜ |

---

## 6. Matriz consolidada (entrega 10/jun)

| Critério | Status | Teste |
|----------|--------|-------|
| Pipeline MiniPar OO em microsserviços | ✅ | E1 |
| Erro sintático (parser) | ✅ | **E7** |
| Erro semântico | ✅ | E8 |
| Template Method (6+ back-ends) | ✅ | E2, E5, E6, E9 |
| `gcc -O2` C/C++ | ✅ | E5, E12 |
| `rustc` no MS Rust | ✅ | **E6** |
| Interpretador OO + fractal | ✅ | E2, E3 |
| Teste 3 máquinas via sockets | ✅ | E4, E10 |
| `PAR` + canais socket | ✅ | E11 |
| Workers executam MiniPar | ✅ | E10 |
| Semântica no MS (`semantic_full`) | ✅ | E8 |
| LPS `GET /variants` + recomendações | ✅ | API |
| Frontend + painel MS | ✅ | código |
| Relatório + figuras | ✅ | `report.md`/`report.tex` |
| Validação automatizada | ✅ | 15/15 |
| Back-end ARM E2E | 🟡 | sem caso no script |
| Tipagem semântica plena | 🟡 | MVP |
| 3 PCs físicos | 🟡 | containers |
| PDF Overleaf + vídeo | 🟡 | operacional |
| CI pytest | ❌ | não implementado |
| FeatureIDE | ❌ | substituído por MS (documentado) |

---

## 7. Pendências para ajuste (prioridade)

### Alta (antes da banca)

1. **Vídeo backup** — gravar demo com E1–E12 na UI.
2. **Ensaio** — [docs/BANCA_NARRATIVE.md](./docs/BANCA_NARRATIVE.md).
3. **Overleaf (opcional)** — `./scripts/package-overleaf.sh` se quiser editar no navegador.

### Média (melhoria de conformidade)

4. Adicionar **E_ARM** opcional ao `validate-all.sh` se toolchain ARM estiver no container.
5. Expandir **semântica** (tipos de parâmetros, retorno).

### Baixa / pós-entrega

6. `pytest` no CI; hotspots lexer/parser alternativos; `minipar_rt` em Rust/ARM.

---

## 8. Feito diferente do pedido (transparência na banca)

| Expectativa | Implementação real |
|-------------|-------------------|
| Gateway Spring Boot | NestJS |
| FeatureIDE | Microsserviços + registry + UI |
| Menu só na UI Angular | **Também** `14_distributed_menu.minipar` |
| Três PCs físicos | Três containers Docker |
| Interpretador para “checar sintaxe” | Parser dedicado (correto) + semântica |
| Toolchain no host do aluno | `gcc`/`rustc` **dentro dos MS** |
| `.exe` Windows | binário Linux no container |

---

## 9. Sincronização de documentos

Ao alterar código ou validação, atualizar **nesta ordem**:

1. `./scripts/validate-all.sh` (se novo caso)
2. **`COMPLIANCE_AUDIT.md`** (este arquivo)
3. **`docs/VALIDATION.md`**
4. **`ACTIVITIES.md`** (checklist E1–E12)
5. **`report.md`** e **`report.tex`** (§7 testes + limitações)
6. **`docs/WHAT_REMAINS.md`** (só pendências operacionais)

---

## 10. Roteiro de demo (10/jun)

| # | Exemplo | Modo LPS | ID |
|---|---------|----------|-----|
| 1 | `08_interpreter_ok` | INTERPRETER · LOCAL | E1 |
| 2 | `09_oo_new` | INTERPRETER · LOCAL | E2 |
| 3 | `13_sierpinski` | INTERPRETER · LOCAL | E3 |
| 4 | `14_distributed_menu` | INTERPRETER · DISTRIBUTED_SOCKETS | E10 |
| 5 | `11_codegen_c` | C · LOCAL | E5 |
| 6 | `12_codegen_rust_stub` | RUST · LOCAL | E6 |
| 7 | `16_codegen_python` | PYTHON · LOCAL | E9 |
| 8 | `05_parse_extends_missing` | INTERPRETER · LOCAL (erro) | E7 |
| 9 | `15_channels` | INTERPRETER · LOCAL | E11 |

---

## Histórico de revisões

| Data | Alteração |
|------|-----------|
| 2026-06-02 | Criação inicial |
| 2026-06-08 | Conformidade técnica fases 1–7; canais, workers MiniPar |
| 2026-06-08 | **Regeneração pós 15/15** — E6 Rust, E7 parser; matriz e §8 corrigidos |
