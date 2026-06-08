# ms-codegen-python

Microsserviço da **extensão demo** MiniPar → Python (`PYTHON`).

- `POST /generate` — recebe AST JSON, chama `PythonBackend().translate()`
- Porta: **3008**
- Registry: `MS_CODEGEN_PYTHON_URL`

Implementação do hotspot: [`packages/minipar-core/minipar_core/translation/python_backend.py`](../../packages/minipar-core/minipar_core/translation/python_backend.py)
