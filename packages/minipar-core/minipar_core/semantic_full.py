"""Análise semântica completa a partir de AST JSON."""

from __future__ import annotations

from minipar_core.semantic import SemanticAnalyzer
from minipar_core.translation.ast_from_json import from_dict


def analyze_ast_full(ast_dict: dict) -> tuple[dict, dict, list[str]]:
    """Retorna (ast, symbol_table_json, errors) usando SemanticAnalyzer."""
    program = from_dict(ast_dict)
    analyzer = SemanticAnalyzer()
    ok = analyzer.analyze(program)
    return ast_dict, analyzer.symbol_table.to_json(), [] if ok else analyzer.errors
