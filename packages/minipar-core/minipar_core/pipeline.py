"""API de alto nível para parse e análise semântica."""

import re

from minipar_core.ast_json import to_dict
from minipar_core.lexer import Lexer
from minipar_core.parser import Parser
from minipar_core.semantic import SemanticAnalyzer


def _parse_error_dict(exc: Exception) -> dict:
    msg = str(exc)
    match = re.search(r"at (\d+):(\d+)", msg)
    line = int(match.group(1)) if match else 1
    column = int(match.group(2)) if match else 1
    return {"line": line, "column": column, "message": msg}


def parse_source(source_code: str) -> tuple[dict | None, list[dict]]:
    try:
        tokens = Lexer(source_code).tokenize()
        ast = Parser(tokens).parse()
        return to_dict(ast), []
    except SyntaxError as exc:
        return None, [_parse_error_dict(exc)]


def analyze_program(source_code: str) -> tuple[dict | None, dict | None, list[str]]:
    try:
        tokens = Lexer(source_code).tokenize()
        ast = Parser(tokens).parse()
        analyzer = SemanticAnalyzer()
        ok = analyzer.analyze(ast)
        ast_json = to_dict(ast)
        symbol_table = analyzer.symbol_table.to_json()
        return ast_json, symbol_table, [] if ok else analyzer.errors
    except SyntaxError as exc:
        return None, None, [str(exc)]
