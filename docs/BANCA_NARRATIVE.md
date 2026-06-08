# Roteiro de banca — MiniPar Framework 2026.1

Roteiro para apresentação oral (~15–20 min) respondendo à crítica do Prof. Arturo: *framework vs gerador de aplicações*.

## Mensagem central (30 segundos)

> *"Nosso projeto é um **framework LPS** com frozen-spots (pipeline, `translate()`) e hotspots (`emit()`, `finalize()`). As cinco variantes existentes são **instâncias de referência** — não um gerador fechado. A extensão **Python** prova que um dev adiciona back-end sem alterar o esqueleto."*

## Bloco 1 — Framework vs gerador (3 min)

1. Mostrar tabela do relatório (Parte II): gerador gera pasta independente; framework mantém `minipar-core` em runtime.
2. Abrir `base_translator.py` → `translate()` é **frozen-spot** (nunca sobrescrever).
3. Abrir `c_backend.py` → `emit()` é **hotspot** (código do dev: TAC + gcc).
4. Diagrama: `docs/figures/template-method.png`

**Frase-chave:** *"O framework chama `emit()` — Hollywood Principle. O dev não chama `translate()`."*

## Bloco 2 — Três instâncias de referência (5 min)

### Instância A — Interpretador

- UI: variante **Interpretador** + LOCAL
- Exemplo: `08_interpreter_ok.minipar` → saída `ok`
- Mostrar: `applications/reference-interpreter/README.md`
- Hotspot: execução direta AST (~500 linhas em `interpreter.py`)

### Instância B — Compilador C

- UI: variante **C** + LOCAL
- Exemplo: `11_codegen_c.minipar` → C + `gcc -O2`
- Mostrar: `applications/reference-compiler-c/README.md`
- Hotspot: TAC → C → compilação

### Instância C — Extensão Python (demo ao vivo)

- UI: variante **Python (extensão)** + LOCAL
- Exemplo: `16_codegen_python.minipar`
- Mostrar diff mínimo em `applications/extension-python/README.md`
- Executar ao vivo → código Python + stdout

**Frase-chave:** *"Trocamos apenas o microsserviço de tradução; lexer, parser e semântica permanecem invariantes."*

## Bloco 3 — Como criar nova aplicação (3 min)

1. Abrir `CREATING_AN_APPLICATION.md` — 6 passos numerados.
2. Mostrar `_template_backend.py` (hotspots vazios com `NotImplementedError`).
3. Mostrar `backend-registry.ts` — adicionar variante = 1 linha.
4. Responder: *"Não precisamos de `createProject`. Configuramos stack + hotspots + registry."*

## Bloco 4 — LPS e frontend (2 min)

1. Feature panel = **configuração de produto**, não hotspot de algoritmo.
2. Diagrama: `docs/figures/feature-tree.png`
3. Opcional: `GET /api/v1/variants` — variantes dinâmicas do registry.
4. Qualquer cliente HTTP (curl, CLI) pode usar o framework sem Angular.

## Bloco 5 — Compiladores + reuso (3 min)

1. BNF completa no relatório (Parte III).
2. Template Method profundo (Parte IV) — frozen vs hot.
3. Mapa de reuso 2025.1 → 2026.1: `docs/figures/reuse-map.png`

## Bloco 6 — Testes obrigatórios (3 min)

| Teste | Exemplo | Modo |
|-------|---------|------|
| Fractal Sierpinski | `13_sierpinski.minipar` | INTERPRETER + LOCAL |
| 3 máquinas | qualquer fonte válida | DISTRIBUTED_SOCKETS |
| OO + C | `09_oo_new.minipar` | C + LOCAL |
| Extensão Python | `16_codegen_python.minipar` | PYTHON + LOCAL |

**Honestidade:** `PAR` local usa threads; sockets no teste dedicado; workers Python fixos.

## Perguntas esperadas

| Pergunta | Resposta |
|----------|----------|
| "É gerador ou framework?" | Framework — instanciação via hotspots + registry, não scaffolding |
| "Onde está o código do dev?" | `c_backend.py`, `interpreter.py`, `python_backend.py` |
| "Hotspot = método abstrato?" | Abstrato = contrato; hotspot = corpo que implementa |
| "Por que comentar hotspots?" | Não comentamos — instâncias funcionam; template vazio separado |
| "FeatureIDE?" | LPS por microsserviços + feature tree + Docker Compose |
| "Spring Boot?" | NestJS — mesma função de gateway |

## Checklist pré-banca

- [ ] `docker compose up --build` — stack verde
- [ ] Exemplos 08, 11, 13, 16 funcionam na UI
- [ ] `DISTRIBUTED_SOCKETS` agrega PC1–PC3
- [ ] Relatório PDF com figuras exportadas
- [ ] Vídeo backup gravado

## Ordem sugerida de demo ao vivo

1. Interpretador OK (08)
2. Compilador C (11)
3. Fractal (13)
4. **Extensão Python (16)** — destaque
5. 3 máquinas (DISTRIBUTED_SOCKETS)
6. Erro semântico (04) — mostrar diagnóstico
