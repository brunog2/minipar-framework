# ms-codegen-rust

## Responsabilidade

Gerar código **Rust** equivalente à AST e compilar com `rustc` (otimização recomendada: release).

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| `POST` | `/generate` | Gera Rust + build opcional |
| `GET` | `/health` | Health check |

## Contrato de entrada

```json
{
  "ast": { "type": "Program", "declarations": [] },
  "symbolTable": {},
  "executionMode": "LOCAL",
  "target": "RUST"
}
```

## Contrato de saída

```json
{
  "output": "Build Rust OK",
  "code": "fn main() { ... }"
}
```

## Reuso de software

**Novo componente** — não existe nas referências atuais. Implementar via **Template Method** compartilhando esqueleto com `ms-codegen-c` (hotspot: `emitFunction`, `emitClass`, etc.).

## Variabilidade LPS

| Ponto de variação | Variante |
|-------------------|----------|
| Back-end | **RUST** |

## Status

**Não implementado** nesta fase de setup.
