# ms-codegen-rust

## Responsabilidade

Gerar código **Rust** equivalente à AST e compilar com `rustc` quando disponível.

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| `POST` | `/generate` | Gera Rust + build opcional |
| `GET` | `/health` | Health check |

## Contrato de saída

```json
{
  "output": "Build Rust OK\n...",
  "code": "fn main() { ... }"
}
```

Se `rustc` não estiver instalado no host: `output` informa claramente; `code` ainda é retornado. No **Docker Compose**, o image instala `rustc`/`cargo` via `apt` (mesmo padrão do `gcc` em `ms-codegen-c`).

## Reuso de software

Implementado via **Template Method** (`RustBackend`) em `packages/minipar-core/minipar_core/translation/rust_backend.py`.

## Status

**Implementado MVP** (Fase 2 — jun/2026). Porta **3005**.
