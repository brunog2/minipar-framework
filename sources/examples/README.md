# Exemplos MiniPar — validação manual

## Fase 1 — Análise estática

| Arquivo | Resultado esperado |
|---------|-------------------|
| `01_empty_class.minipar` | Sucesso — `ClassDecl` + symbolTable |
| `02_class_extends.minipar` | Sucesso — herança `Dog extends Animal` |
| `03_print_global.minipar` | Sucesso — `PrintStmt` global |
| `04_semantic_extends_unknown.minipar` | Erro semântico — superclasse inexistente |
| `05_parse_extends_missing.minipar` | Erro sintático — `Expected superclass name` |
| `06_parse_invalid_keyword.minipar` | Erro sintático — `Expected LBRACE` |
| `07_expr_only.minipar` | Sucesso — expressão solta (`a`) na análise estática; com **INTERPRETER**, runtime: `Undefined variable: a` |

## Fase 2 — Back-ends reais

Requer `PIPELINE_BACKEND_MODE=http` no gateway (padrão no Docker Compose).

| Arquivo | LPS | Resultado esperado |
|---------|-----|-------------------|
| `08_interpreter_ok.minipar` | INTERPRETER | Saída: `ok` |
| `09_oo_new.minipar` | INTERPRETER | Saída: `woof` (`new Dog()` + método) |
| `10_par_seq.minipar` | INTERPRETER | Saída: `a`, `b`, `c` (seq + par) |
| `11_codegen_c.minipar` | C | C gerado + `gcc -O2` + stdout |
| `12_codegen_rust_stub.minipar` | RUST | Código Rust mínimo (+ rustc se disponível) |

Testar na UI (http://localhost:4200) com **Executar** ou `Ctrl+Enter` / `F5`.

```bash
curl -s -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"sourceCode":"class Main { void run() { println(\"ok\"); } }",
       "targetVariability":"INTERPRETER","executionMode":"LOCAL"}'
```

## Fase 3 — Paralelismo distribuído + fractal

| Arquivo | Modo | Resultado esperado |
|---------|------|-------------------|
| `13_sierpinski.minipar` | INTERPRETER + LOCAL | Matriz 27×27 do tapete de Sierpinski (`.` e `*`) |
| `14_distributed_menu.minipar` | INTERPRETER + DISTRIBUTED_SOCKETS | QuickSort (PC1), Matriz (PC2), Fatorial (PC3) via sockets |
| `09_oo_new.minipar` | C + LOCAL | OO compilado com `gcc -O2` → saída `woof` |

```bash
# Fractal
curl -s -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"sourceCode":"'"$(cat sources/examples/13_sierpinski.minipar | sed 's/"/\\"/g' | tr '\n' ' ')"'",
       "targetVariability":"INTERPRETER","executionMode":"LOCAL"}'

# 3 máquinas
curl -s -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"sourceCode":"class Main { void run() { println(\"ok\"); } }",
       "targetVariability":"INTERPRETER","executionMode":"DISTRIBUTED_SOCKETS"}'
```

Pipeline steps Fase 3 (distribuído): `ms-front-end: parse`, `ms-semantic: analyze`, `ms-parallel-coord: coordinate`, `ms-interpreter: execute`.
