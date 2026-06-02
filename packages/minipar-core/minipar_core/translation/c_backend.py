"""Back-end C/C++ — TAC → C → gcc -O2."""

from __future__ import annotations

import os
import subprocess
import tempfile
import uuid
from pathlib import Path

from minipar_core.translation.base_translator import (
    AbstractBackendTranslator,
    TranslationResult,
)
from minipar_core.translation.c_codegen import SimpleCCodeGenerator
from minipar_core.translation.tac_codegen import TACGenerator


class CBackend(AbstractBackendTranslator):
    compiler = "gcc"
    std_flag = "-std=c11"

    def __init__(self) -> None:
        self._code = ""
        self._output = ""
        self._exit_code = 0

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

    def _compile_and_run(self, c_code: str) -> dict:
        work = Path(tempfile.gettempdir()) / f"minipar-{uuid.uuid4().hex[:8]}"
        work.mkdir(parents=True, exist_ok=True)
        c_file = work / "program.c"
        exe_file = work / "program"

        try:
            c_file.write_text(c_code, encoding="utf-8")
            compile_cmd = [
                self.compiler,
                f"-O2",
                self.std_flag,
                str(c_file),
                "-o",
                str(exe_file),
                "-lm",
            ]
            comp = subprocess.run(
                compile_cmd, capture_output=True, text=True, check=False
            )
            if comp.returncode != 0:
                msg = comp.stderr or comp.stdout or "gcc failed"
                return {
                    "output": f"GCC compilation failed:\n{msg}",
                    "exit_code": comp.returncode,
                }

            run = subprocess.run(
                [str(exe_file)], capture_output=True, text=True, check=False, timeout=30
            )
            stdout = run.stdout or ""
            stderr = run.stderr or ""
            log = f"Compiled with {self.compiler} -O2\n"
            if stdout:
                log += stdout
            if stderr:
                log += stderr
            return {"output": log, "exit_code": run.returncode}
        except FileNotFoundError:
            return {
                "output": f"{self.compiler} not found. Install build-essential (gcc).",
                "exit_code": 1,
            }
        finally:
            for p in (c_file, exe_file):
                try:
                    p.unlink(missing_ok=True)
                except OSError:
                    pass
            try:
                work.rmdir()
            except OSError:
                pass


class CppBackend(CBackend):
    compiler = "g++"
    std_flag = "-std=c++17"


def generate_c(ast_dict: dict, target: str = "C") -> TranslationResult:
    backend: CBackend = CppBackend() if target == "CPP" else CBackend()
    return backend.translate(ast_dict)
