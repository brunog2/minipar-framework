# TEMPLATE DE EXTENSÃO — copie para meu_backend.py e preencha os hotspots
# Framework: AbstractBackendTranslator (base_translator.py)
# Hotspots a implementar: emit(), finalize()
# Não sobrescreva translate(), validate() nem prepare() — são frozen-spots

"""Esqueleto vazio para novo back-end MiniPar — preencha os hotspots."""

from __future__ import annotations

from minipar_core.translation.base_translator import (
    AbstractBackendTranslator,
    TranslationResult,
)


class TemplateBackend(AbstractBackendTranslator):
    """Copie esta classe, renomeie e implemente emit() / finalize()."""

    def __init__(self) -> None:
        self._output = ""
        self._code = ""

    def hook_validate(self, ast_dict: dict) -> None:
        # Hotspot opcional: validações específicas do seu back-end
        if not ast_dict.get("declarations"):
            self._errors.append("Programa vazio: nenhuma declaração encontrada")

    def hook_prepare(self, ast_dict: dict) -> None:
        # Hotspot opcional: pré-processamento antes de emit()
        pass

    def emit(self, ast_dict: dict) -> None:
        # TODO: seu algoritmo aqui — transformar ast_dict em artefato de saída
        raise NotImplementedError("Implemente emit(): TAC, AST direta, bytecode, etc.")

    def finalize(self) -> TranslationResult:
        # TODO: montar TranslationResult com output, code e exit_code
        raise NotImplementedError("Implemente finalize(): retorne TranslationResult")


def generate_template(ast_dict: dict) -> TranslationResult:
    return TemplateBackend().translate(ast_dict)
