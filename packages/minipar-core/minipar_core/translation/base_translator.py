"""Template Method — esqueleto comum de tradução AST → back-end."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TranslationResult:
    output: str
    code: str | None = None
    exit_code: int = 0
    errors: list[str] = field(default_factory=list)


class AbstractBackendTranslator(ABC):
    """Esqueleto fixo: validate → prepare → emit → finalize (hotspots em emit)."""

    def translate(self, ast_dict: dict) -> TranslationResult:
        self._errors: list[str] = []
        self.validate(ast_dict)
        if self._errors:
            return TranslationResult(
                output="; ".join(self._errors),
                exit_code=1,
                errors=list(self._errors),
            )
        self.prepare(ast_dict)
        self.emit(ast_dict)
        return self.finalize()

    def validate(self, ast_dict: dict) -> None:
        """Frozen-spot: validação base da AST. Não sobrescrever.

        Verifica que a AST tem raiz 'Program'. Ao final delega ao hook
        opcional hook_validate() para que backends adicionem validações
        específicas sem precisar copiar a lógica base.
        """
        if not ast_dict or ast_dict.get("type") != "Program":
            self._errors.append("AST inválida: raiz deve ser Program")
        self.hook_validate(ast_dict)

    def hook_validate(self, ast_dict: dict) -> None:
        """Hot-spot opcional: backends sobrescrevem para validações específicas.

        Chamar self._errors.append(...) para reportar erros adicionais.
        Implementação padrão é no-op.
        """
        pass

    def prepare(self, ast_dict: dict) -> None:
        """Frozen-spot: armazena AST para uso em emit(). Não sobrescrever.

        Ao final delega ao hook opcional hook_prepare() para que backends
        realizem pré-processamento sem necessidade de sobrescrever prepare().
        """
        self._ast = ast_dict
        self.hook_prepare(ast_dict)

    def hook_prepare(self, ast_dict: dict) -> None:
        """Hot-spot opcional: backends sobrescrevem para pré-processamento.

        Executado após self._ast ser definido. Implementação padrão é no-op.
        """
        pass

    @abstractmethod
    def emit(self, ast_dict: dict) -> None:
        """Hotspot principal — implementado por cada back-end.

        Garantias do framework (frozen-spots):
        - ast_dict['type'] == 'Program'  (validado antes de emit() ser chamado)
        - ast_dict está disponível em self._ast após prepare()

        Responsabilidade do backend:
        - Transformar ast_dict no artefato de saída
        - Armazenar resultado intermediário em atributo de instância
        - NÃO lançar exceções — reportar erros via self._errors.append(msg)
        """

    @abstractmethod
    def finalize(self) -> TranslationResult:
        """Hotspot de saída — monta TranslationResult.

        Chamado após emit(). Responsabilidade do backend:
        - Retornar TranslationResult(output=..., code=..., exit_code=...)
        - output: string exibida ao usuário (stdout do programa, mensagens, etc.)
        - code: código-fonte gerado (opcional, None para interpretadores)
        - exit_code: 0 para sucesso, != 0 para erro
        """
