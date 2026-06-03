from minipar_core.pipeline import parse_source, analyze_program
from minipar_core.ast_json import to_dict
from minipar_core.semantic_json import analyze_ast_dict
from minipar_core.translation import (
    interpret_ast,
    generate_c,
    generate_rust,
    generate_arm,
)


def interpret_source(source_code: str, print_hook=None) -> dict:
    """Execute MiniPar source code and return result. print_hook captures print output."""
    from minipar_core.lexer import Lexer
    from minipar_core.parser import Parser
    from minipar_core.translation.interpreter import Interpreter

    tokens = Lexer(source_code).tokenize()
    program = Parser(tokens).parse()
    interp = Interpreter()
    if print_hook is not None:
        interp._print_hook = print_hook
    try:
        output = interp.execute(program)
        return {"status": "ok", "output": output}
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


__all__ = [
    "parse_source",
    "analyze_program",
    "analyze_ast_dict",
    "to_dict",
    "interpret_ast",
    "generate_c",
    "generate_rust",
    "generate_arm",
    "interpret_source",
]
