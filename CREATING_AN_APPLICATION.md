# Como criar uma nova aplicação (instância) a partir do MiniPar Framework

Este guia responde à pergunta da banca: *"Como criar uma nova aplicação a partir do framework?"* — no sentido do Prof. Arturo: **montar uma instância LPS** reutilizando frozen-spots e preenchendo hotspots, **não** gerar um repositório independente.

## 1. Definições

| Termo | Significado no MiniPar |
|-------|------------------------|
| **Framework** | Infraestrutura invariante: lexer, parser, semântica, `translate()`, gateway, contratos REST |
| **Instância / aplicação** | Configuração LPS: microsserviços ativos + hotspot de tradução implementado |
| **Frozen-spot** | Código que o dev **não** sobrescreve (`translate()`, pipeline do gateway) |
| **Hotspot** | Corpo que o dev **escreve** dentro do contrato (`emit()`, `finalize()`) |
| **Variante LPS** | Valor de `targetVariability` (ex.: `C`, `PYTHON`) selecionado na UI |

## 2. Mapa do repositório

```
Framework (frozen-spots)          Instância (hotspots do dev)
─────────────────────────         ────────────────────────────
packages/minipar-core/            translation/*_backend.py
  lexer.py, parser.py               emit(), finalize()
  base_translator.py
api-gateway/                      backend-registry.ts (+1 linha)
  pipeline.service.ts             microservices/ms-codegen-*/
ms-front-end, ms-semantic         (thin wrapper FastAPI)
frontend/                         feature-panel (+1 radio button)
```

Catálogo de instâncias existentes: [applications/README.md](applications/README.md).

## 3. Passo a passo — exemplo: Compilador MiniPar → Go

### Passo 1 — Reusar o chassi

Mantenha ativos: `minipar-core`, `api-gateway`, `ms-front-end`, `ms-semantic`, `frontend`. Não altere `translate()` nem o pipeline.

### Passo 2 — Criar o back-end (hotspot)

Copie o template:

```bash
cp packages/minipar-core/minipar_core/translation/_template_backend.py \
   packages/minipar-core/minipar_core/translation/go_backend.py
```

Implemente `emit()` e `finalize()`:

```python
class GoBackend(AbstractBackendTranslator):
    def emit(self, ast_dict: dict) -> None:
        tac = TACGenerator().lower(ast_dict)
        self._code = self._tac_to_go(tac)  # seu algoritmo

    def finalize(self) -> TranslationResult:
        return TranslationResult(output="Go gerado.", code=self._code, exit_code=0)
```

Exporte em `translation/__init__.py`: `generate_go(ast_dict)`.

### Passo 3 — Criar microsserviço

Espelhe `microservices/ms-codegen-c/` (~30 linhas):

```python
@app.post("/generate")
def generate(body: GenerateRequest):
    result = generate_go(body.ast)
    return GenerateResponse(output=result.output, code=result.code)
```

### Passo 4 — Registrar no gateway (OCP)

```typescript
// backend-registry.ts — uma linha:
{ variability: 'GO', envKey: 'MS_CODEGEN_GO_URL', endpoint: '/generate', mockLabel: 'Codegen Go' }
```

Adicione no `docker-compose.yml`:

```yaml
MS_CODEGEN_GO_URL: http://ms-codegen-go:3009
```

### Passo 5 — Expor na UI (configuração LPS)

| Arquivo | Alteração |
|---------|-----------|
| `feature-panel.component.ts` | `{ value: 'GO', label: 'Compilador → Go' }` |
| `process.models.ts` | `'GO'` no type `TargetVariability` |
| `target-variability.enum.ts` | `GO = 'GO'` |

Isso **não** é escrever algoritmo de compilação — é expor a variante para o usuário selecionar.

### Passo 6 — Instância pronta

Mesma UI, mesma gramática, mesma AST — saída em Go.

## 4. Frontend como casca LPS (frozen-spot)

O Angular em `frontend/` **não** implementa hotspots de compilador. É a **instância de referência da UI LPS**:

| Componente | Papel |
|------------|-------|
| `code-editor` | Editor de código MiniPar |
| `feature-panel` | Seleção de variante LPS (binding runtime) |
| `compiler-workspace` | `POST /api/v1/process` |
| `output-panel` | Exibição de saída |

Qualquer cliente HTTP pode substituir o Angular:

```bash
curl -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"sourceCode":"...", "targetVariability":"PYTHON", "executionMode":"LOCAL"}'
```

### Evolução opcional: `GET /api/v1/variants`

O gateway expõe variantes registradas dinamicamente (OCP completo na UI):

```bash
curl http://localhost:3000/api/v1/variants
# [{ "variability": "C", "label": "Codegen C" }, ...]
```

## 5. FAQ da banca

**Onde coloco meu algoritmo?**  
Em `emit()` e `finalize()` da sua classe que estende `AbstractBackendTranslator`.

**Posso colocar logs customizados?**  
Sim. Ex.: `CBackend._compile_and_run()` registra saída do `gcc -O2`.

**Preciso alterar o gateway?**  
Não. Apenas 1 linha no `BACKEND_REGISTRY`.

**Método abstrato vs hotspot — qual a diferença?**  
Método abstrato = contrato (assinatura fixa, sem implementação). Hotspot = corpo que o dev escreve. Frozen-spot = `translate()` — o framework controla a ordem.

**Por que parece um gerador na demo?**  
Porque todas as variantes já foram implementadas pela equipe. A extensão Python (`applications/extension-python/`) demonstra o processo de adicionar uma nova.

**Duas aplicações distintas?**  
Sim — Interpretador (`INTERPRETER`) e Compilador C (`C`) são duas instâncias sobre o mesmo chassi. Só muda o microsserviço de tradução e os hotspots `emit`/`finalize`.

## 6. Resposta explícita ao Arturo

> *"Fornecemos a estrutura; o dev preenche os hotspots."*

- A estrutura está em `minipar-core` + gateway + MS de análise.
- O código do dev **já existe** nas instâncias de referência (`c_backend.py`, `interpreter.py`, …).
- Para provar extensão nova, adicionamos `PythonBackend` sem alterar frozen-spots.
- Hotspots futuros em lexer/parser estão documentados como roadmap; MVP usa implementação default.

## 7. Referências

- [EXTENDING.md](packages/minipar-core/EXTENDING.md) — contrato técnico dos hotspots
- [applications/](applications/) — catálogo de instâncias
- [_template_backend.py](packages/minipar-core/minipar_core/translation/_template_backend.py) — esqueleto vazio
- [BANCA_NARRATIVE.md](docs/BANCA_NARRATIVE.md) — roteiro de apresentação
