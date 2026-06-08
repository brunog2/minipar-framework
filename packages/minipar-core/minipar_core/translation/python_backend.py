# EXTENSÃO NOVA (demo banca): Compilador MiniPar → Python
# Framework: AbstractBackendTranslator (base_translator.py)
# Hotspots implementados neste arquivo: emit(), finalize()
# O dev desta aplicação escolheu: TAC → Python → python3

"""Back-end Python — TAC → Python → execução com python3."""

from __future__ import annotations

import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Dict, List

from minipar_core.translation.base_translator import (
    AbstractBackendTranslator,
    TranslationResult,
)
from minipar_core.translation.tac import TAC
from minipar_core.translation.tac_codegen import TACGenerator


class SimplePythonCodeGenerator:
    """Gera Python executável para subset MVP: print, funções, main entry."""

    def __init__(self) -> None:
        self.functions: Dict[str, List[str]] = {}
        self.current_fn: str | None = None
        self.fn_body: List[str] = []
        self.main_body: List[str] = []
        self.pending_params: List[str] = []

    def _target_body(self) -> List[str]:
        if self.current_fn:
            return self.fn_body
        return self.main_body

    def _emit(self, line: str) -> None:
        self._target_body().append(line)

    def _literal(self, value) -> str:
        if value is None:
            return "None"
        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                return value
            return repr(value)
        return str(value)

    def generate(self, instructions: List[TAC]) -> str:
        self.functions = {}
        self.current_fn = None
        self.fn_body = []
        self.main_body = []
        self.pending_params = []

        for instr in instructions:
            op = instr.op

            if op == "FUNC_BEGIN":
                self.current_fn = str(instr.arg1)
                self.fn_body = []
                self.pending_params = []
                continue

            if op == "FUNC_PARAM":
                self.pending_params.append(str(instr.arg1))
                continue

            if op == "FUNC_END":
                fn = self.current_fn or "unknown"
                params = ", ".join(self.pending_params) if self.pending_params else ""
                self.functions[fn] = [
                    f"def {fn}({params}):",
                    *[f"    {line}" for line in self.fn_body],
                ]
                self.current_fn = None
                self.fn_body = []
                self.pending_params = []
                continue

            if op == "ASSIGN":
                self._emit(f"{instr.result} = {self._literal(instr.arg1)}")
                continue

            if op in ("ADD", "SUB", "MUL", "DIV"):
                self._emit(
                    f"{instr.result} = {instr.arg1} {instr.op.lower()} {instr.arg2}"
                )
                continue

            if op == "UNARY":
                self._emit(f"{instr.result} = {instr.arg2}{instr.arg1}")
                continue

            if op == "PRINT":
                newline = instr.arg2 == "1"
                arg = self._literal(instr.arg1)
                if newline:
                    self._emit(f"print({arg})")
                else:
                    self._emit(f"print({arg}, end='')")
                continue

            if op == "CALL":
                args = instr.arg2 or ""
                self._emit(f"{instr.result} = {instr.arg1}({args})")
                continue

            if op == "CALL_MAIN":
                self._emit("Main_run()")
                continue

            if op == "RETURN":
                if instr.arg1 is not None:
                    self._emit(f"return {instr.arg1}")
                else:
                    self._emit("return")
                continue

            if op == "LABEL":
                self._emit(f"# {instr.arg1}:")
                continue

            if op in ("GOTO", "IF_FALSE", "IF_TRUE"):
                self._emit(f"# {instr}")
                continue

        lines = [
            '"""Gerado pelo MiniPar PythonBackend (extensão demo)."""',
            "",
        ]
        for fn_lines in self.functions.values():
            lines.extend(fn_lines)
            lines.append("")
        lines.append('if __name__ == "__main__":')
        if self.main_body:
            for line in self.main_body:
                lines.append(f"    {line}")
        else:
            lines.append("    Main_run()")
        return "\n".join(lines) + "\n"


class PythonBackend(AbstractBackendTranslator):
    """Extensão demo: emite Python a partir de TAC e executa com python3."""

    def __init__(self) -> None:
        self._code = ""

    def emit(self, ast_dict: dict) -> None:
        tac = TACGenerator().lower(ast_dict)
        self._code = SimplePythonCodeGenerator().generate(tac)

    def finalize(self) -> TranslationResult:
        result = self._run_python(self._code)
        return TranslationResult(
            output=result["output"],
            code=self._code,
            exit_code=result["exit_code"],
        )

    def _run_python(self, code: str) -> dict:
        work = Path(tempfile.gettempdir()) / f"minipar-py-{uuid.uuid4().hex[:8]}"
        work.mkdir(parents=True, exist_ok=True)
        py_file = work / "program.py"

        try:
            py_file.write_text(code, encoding="utf-8")
            run = subprocess.run(
                ["python3", str(py_file)],
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
            stdout = run.stdout or ""
            stderr = run.stderr or ""
            log = "Executado com python3\n"
            if stdout:
                log += stdout
            if stderr:
                log += stderr
            return {"output": log, "exit_code": run.returncode}
        except FileNotFoundError:
            return {
                "output": "python3 não encontrado. Instale Python 3 no container.",
                "exit_code": 1,
            }
        finally:
            try:
                py_file.unlink(missing_ok=True)
                work.rmdir()
            except OSError:
                pass


def generate_python(ast_dict: dict) -> TranslationResult:
    return PythonBackend().translate(ast_dict)
