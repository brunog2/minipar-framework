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
        if not ast_dict or ast_dict.get("type") != "Program":
            self._errors.append("AST inválida: raiz deve ser Program")

    def prepare(self, ast_dict: dict) -> None:
        self._ast = ast_dict

    @abstractmethod
    def emit(self, ast_dict: dict) -> None:
        """Hotspot principal — implementado por cada back-end."""

    @abstractmethod
    def finalize(self) -> TranslationResult:
        """Hotspot de saída — monta TranslationResult."""
