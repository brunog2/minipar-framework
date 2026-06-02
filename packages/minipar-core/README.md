# minipar-core

Pacote Python compartilhado pelos microsserviços MiniPar 2026.1.

## Módulos

| Módulo | Fase | Descrição |
|--------|------|-----------|
| `lexer.py` | 1 | Análise léxica |
| `parser.py` | 1 | Parser descendente recursivo → AST |
| `ast_nodes.py` | 1 | Nós da AST (OO + `par`/`seq`) |
| `ast_json.py` | 1 | AST → JSON (`_AST_CONTRACT.md`) |
| `semantic.py` / `semantic_json.py` | 1 | Análise semântica + tabela de símbolos |
| `translation/` | 2 | Template Method + back-ends |

## translation/ (Fase 2)

| Arquivo | Papel |
|---------|--------|
| `base_translator.py` | `AbstractBackendTranslator`, `TranslationResult` |
| `ast_from_json.py` | JSON → AST (deserialização para MS) |
| `tac.py`, `tac_codegen.py` | IR TAC (reuso `projeto_compiladores`) |
| `interpreter.py` | Interpretador OO (port `cl-minipar`) |
| `c_backend.py`, `c_codegen.py` | C/C++ + `gcc -O2` |
| `rust_backend.py` | Rust MVP |
| `arm_backend.py` | ARMv7 MVP |

## API pública

```python
from minipar_core import (
    parse_source,
    analyze_ast_dict,
    interpret_ast,
    generate_c,
    generate_rust,
    generate_arm,
)

ast, errors = parse_source(source_code)
result = interpret_ast(ast)        # output: str
c_result = generate_c(ast, "C")    # code + log gcc
```

## Instalação (desenvolvimento)

```bash
pip install -e packages/minipar-core
```

Usado nos Dockerfiles dos microsserviços com `COPY packages/minipar-core`.
