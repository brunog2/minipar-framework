# Guia de Extensão — MiniPar Backend Framework

Este documento descreve o contrato de extensão do MiniPar para criação de novos backends de compilação/interpretação.

---

## 1. Hierarquia de classes

```
AbstractBackendTranslator   (minipar_core/translation/base_translator.py)
├── Interpreter             → execução direta da AST (interprete)
├── CBackend                → geração C + compilação com gcc -O2
│   └── CppBackend          → geração C++ + compilação com g++ -O2 (herda CBackend)
├── RustBackend             → geração Rust + compilação com rustc
├── ARMBackend              → geração Assembly ARMv7
└── SeuNovoBackend          ← você implementa aqui
```

O método `translate(ast_dict)` em `AbstractBackendTranslator` é o **frozen-spot** principal: ele sempre executa a sequência `validate → prepare → emit → finalize`. Você nunca sobrescreve `translate()`.

---

## 2. Contrato dos hotspots

### `emit(ast_dict: dict) -> None` — hotspot obrigatório

```python
@abstractmethod
def emit(self, ast_dict: dict) -> None:
    """
    Hotspot principal. Recebe a AST como dict validado e serializado.

    Garantias do framework (frozen-spots):
    - ast_dict['type'] == 'Program'  (validado antes de emit() ser chamado)
    - ast_dict está disponível em self._ast após prepare()

    Responsabilidade do backend:
    - Transformar ast_dict no artefato de saída
    - Armazenar resultado intermediário em atributo de instância
    - NÃO lançar exceções — reportar erros via self._errors.append(msg)

    Exemplo mínimo:
        def emit(self, ast_dict: dict) -> None:
            self._output = f"// AST recebida com {len(ast_dict)} chaves"
    """
```

### `finalize() -> TranslationResult` — hotspot obrigatório

```python
@abstractmethod
def finalize(self) -> TranslationResult:
    """
    Hotspot de saída. Chamado após emit().

    Responsabilidade do backend:
    - Retornar TranslationResult(output=..., code=..., exit_code=...)
    - output: string exibida ao usuário (stdout do programa, mensagens, etc.)
    - code: código-fonte gerado (opcional, None para interpretadores)
    - exit_code: 0 para sucesso, != 0 para erro

    Exemplo mínimo:
        def finalize(self) -> TranslationResult:
            return TranslationResult(output=self._output, exit_code=0)
    """
```

### `hook_validate(ast_dict: dict) -> None` — hotspot opcional

Chamado ao final de `validate()`. Sobrescreva para adicionar validações específicas do backend sem perder a validação base.

```python
def hook_validate(self, ast_dict: dict) -> None:
    # Verificar que há pelo menos uma declaração
    if not ast_dict.get('declarations'):
        self._errors.append("Programa vazio: nenhuma declaração encontrada")
```

### `hook_prepare(ast_dict: dict) -> None` — hotspot opcional

Chamado ao final de `prepare()`, após `self._ast` ser definido. Use para pré-processamento antes de `emit()`.

```python
def hook_prepare(self, ast_dict: dict) -> None:
    # Pré-indexar todas as classes declaradas
    self._class_names = {
        d['name'] for d in ast_dict.get('declarations', [])
        if d.get('type') == 'ClassDecl'
    }
```

---

## 3. Exemplo completo de novo backend (Python)

```python
# minipar_core/translation/python_backend.py
from minipar_core.translation.base_translator import AbstractBackendTranslator, TranslationResult
from minipar_core.translation.tac_codegen import TACGenerator


class PythonBackend(AbstractBackendTranslator):
    """Exemplo: backend que gera código Python a partir de MiniPar."""

    def emit(self, ast_dict: dict) -> None:
        tac = TACGenerator().lower(ast_dict)
        self._code = self._tac_to_python(tac)

    def finalize(self) -> TranslationResult:
        return TranslationResult(output="Python gerado.", code=self._code, exit_code=0)

    def _tac_to_python(self, tac) -> str:
        # implementar conversão TAC → Python
        return "# MiniPar Python Backend\n"
```

**Princípio geral:** sempre use `TACGenerator().lower(ast_dict)` para obter o IR intermediário. Percorrer a AST diretamente funciona, mas dificulta a manutenção — o TAC já lida com herança, resolução de nomes e expressões compostas.

---

## 4. Como registrar o novo backend no gateway

Adicionar **apenas uma linha** ao registry em `api-gateway/src/pipeline/backend-registry.ts`:

```typescript
// backend-registry.ts — adicionar apenas esta linha:
{ variability: 'PYTHON', envKey: 'MS_CODEGEN_PYTHON_URL', endpoint: '/generate' }
```

O gateway usa `BACKEND_REGISTRY.find(b => b.variability === targetVariability)` para rotear a requisição. Nenhum outro arquivo precisa ser modificado.

Adicionar também no `.env`:
```
MS_CODEGEN_PYTHON_URL=http://ms-codegen-python:8000
```

E criar o microserviço FastAPI expondo `POST /generate` que instancia `PythonBackend().translate(ast_dict)`.

---

## 5. Checklist para novos backends

- [ ] Herda `AbstractBackendTranslator` (de `minipar_core.translation.base_translator`)
- [ ] Implementa `emit(ast_dict: dict) -> None`
- [ ] Implementa `finalize() -> TranslationResult`
- [ ] Usa `TACGenerator().lower(ast_dict)` se possível (não percorrer AST diretamente)
- [ ] Armazena erros via `self._errors.append()`, não lança exceções em `emit`
- [ ] Registrado em `api-gateway/src/pipeline/backend-registry.ts`
- [ ] Microsserviço criado com endpoint `/generate` (ou `/execute` para interpretadores)
- [ ] Variável de ambiente `MS_CODEGEN_<NOME>_URL` definida no `.env`
- [ ] `TranslationResult.exit_code == 0` indica sucesso, `!= 0` indica falha

---

## Fluxo de inversão de controle (Hollywood Principle)

```
PipelineService (gateway)
    → POST /generate  (microsserviço)
        → SeuNovoBackend().translate(ast_dict)   ← framework chama seu código
            → validate()       [frozen-spot]
                → hook_validate()  [hot-spot seu]
            → prepare()        [frozen-spot]
                → hook_prepare()   [hot-spot seu]
            → emit()           [hot-spot seu]     ← você implementa aqui
            → finalize()       [hot-spot seu]     ← você implementa aqui
        ← TranslationResult
    ← { output, code, exit_code }
```

O framework controla **quando** cada método é chamado. Você controla **o que** cada método faz.
