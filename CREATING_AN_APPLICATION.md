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

## 3. Exemplos reais de hotspots criados do zero

Os dois exemplos abaixo estão no repositório, em [`packages/minipar-core/minipar_core/translation/`](packages/minipar-core/minipar_core/translation/). São instâncias LPS de referência: o framework fornece `translate()` (frozen-spot); a equipe preencheu `emit()` e `finalize()` (hotspots).

### Exemplo A — Interpretador (`interpreter.py`)

| Item | Valor |
|------|-------|
| Variante LPS | `INTERPRETER` |
| Microsserviço | `ms-interpreter` (`POST /execute`) |
| Arquivo hotspot | [`interpreter.py`](packages/minipar-core/minipar_core/translation/interpreter.py) |
| Estratégia escolhida | Execução direta da AST (sem TAC, sem codegen) |
| Exemplo MiniPar | [`08_interpreter_ok.minipar`](sources/examples/08_interpreter_ok.minipar) → saída `ok` |

O hotspot `emit()` desserializa a AST, executa o programa e guarda stdout em `self._exec_output`. O `finalize()` monta o `TranslationResult`:

```python
def emit(self, ast_dict: dict) -> None:
    program = from_dict(ast_dict)
    if not isinstance(program, n.Program):
        self._errors.append("Expected Program node")
        return
    try:
        self._exec_output = self.execute(program)
    except RuntimeError as exc:
        self._runtime_errors.append(str(exc))
        self._exec_output = ""

def finalize(self) -> TranslationResult:
    if self._runtime_errors:
        return TranslationResult(
            output="; ".join(self._runtime_errors),
            exit_code=1,
            errors=list(self._runtime_errors),
        )
    return TranslationResult(output=self._exec_output, exit_code=0)
```

O restante do arquivo (~500 linhas) é lógica da instância: ambientes, OO (`new`, métodos, `extends`), blocos `par`/`seq` com processos e broker TCP, canais `s_channel`/`c_channel`. Isso **não** faz parte do contrato do framework — é código livre dentro da instância.

### Exemplo B — Compilador C (`c_backend.py`)

| Item | Valor |
|------|-------|
| Variante LPS | `C` (e `CPP` via `CppBackend`) |
| Microsserviço | `ms-codegen-c` (`POST /generate`) |
| Arquivo hotspot | [`c_backend.py`](packages/minipar-core/minipar_core/translation/c_backend.py) |
| Estratégia escolhida | AST → TAC → C → `gcc -O2` → executável |
| Exemplo MiniPar | [`11_codegen_c.minipar`](sources/examples/11_codegen_c.minipar) → C gerado + stdout |

O hotspot `emit()` gera código C via IR intermediário (TAC). O `finalize()` compila com `gcc -O2` e executa o binário:

```python
def emit(self, ast_dict: dict) -> None:
    gen = TACGenerator()
    tac = gen.lower(ast_dict)
    c_gen = SimpleCCodeGenerator()
    self._code = c_gen.generate(tac)

def finalize(self) -> TranslationResult:
    result = self._compile_and_run(self._code)
    return TranslationResult(
        output=result["output"],
        code=self._code,
        exit_code=result["exit_code"],
    )
```

`_compile_and_run()` (método privado da instância) escreve `program.c`, copia `runtime/minipar_rt.{c,h}`, invoca `gcc -O2` e retorna stdout — comportamento específico desta instância, não do framework.

**Contraste entre as duas instâncias:** mesma AST de entrada, mesmo `translate()` do framework, hotspots diferentes — interpretador executa; compilador C gera artefato + roda toolchain externa.

## 4. Passo a passo — exemplo hipotético: Compilador MiniPar → Go

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

## 5. Frontend como casca LPS (frozen-spot)

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

## 6. FAQ da banca

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
Sim — Interpretador (`INTERPRETER`) e Compilador C (`C`) são duas instâncias sobre o mesmo chassi (ver [§3](#3-exemplos-reais-de-hotspots-criados-do-zero)). Só muda o microsserviço de tradução e os hotspots `emit`/`finalize`.

## 7. Resposta explícita ao Arturo

> *"Fornecemos a estrutura; o dev preenche os hotspots."*

- A estrutura está em `minipar-core` + gateway + MS de análise.
- O código do dev **já existe** nas instâncias de referência documentadas no [§3](CREATING_AN_APPLICATION.md#3-exemplos-reais-de-hotspots-criados-do-zero) (`interpreter.py`, `c_backend.py`, …).
- Para provar extensão nova, adicionamos `PythonBackend` sem alterar frozen-spots.

## 8. Referências

- [EXTENDING.md](packages/minipar-core/EXTENDING.md) — contrato técnico dos hotspots
- [applications/](applications/) — catálogo de instâncias
- [_template_backend.py](packages/minipar-core/minipar_core/translation/_template_backend.py) — esqueleto vazio
- [interpreter.py](packages/minipar-core/minipar_core/translation/interpreter.py) · [c_backend.py](packages/minipar-core/minipar_core/translation/c_backend.py) — hotspots reais (§3)
