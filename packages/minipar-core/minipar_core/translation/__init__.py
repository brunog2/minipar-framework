"""Back-ends de tradução — Template Method (Fase 2)."""

from minipar_core.translation.base_translator import TranslationResult
from minipar_core.translation.ast_from_json import from_dict
from minipar_core.translation.interpreter import InterpreterBackend, interpret_ast
from minipar_core.translation.c_backend import CBackend, CppBackend, generate_c
from minipar_core.translation.rust_backend import RustBackend, generate_rust
from minipar_core.translation.arm_backend import ARMBackend, generate_arm

__all__ = [
    "TranslationResult",
    "from_dict",
    "InterpreterBackend",
    "interpret_ast",
    "CBackend",
    "CppBackend",
    "generate_c",
    "RustBackend",
    "generate_rust",
    "ARMBackend",
    "generate_arm",
]
