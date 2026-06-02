"""Three-Address Code — IR compartilhado (port de projeto_compiladores)."""

from __future__ import annotations


class TAC:
    def __init__(self, op: str, arg1=None, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self) -> str:
        if self.op == "CALL":
            return f"{self.op} {self.arg1} {self.arg2} {self.result}"
        if self.op == "PRINT":
            return f"{self.op} {self.arg1} newline={self.arg2}"
        if self.op in (
            "LABEL",
            "GOTO",
            "PARAM",
            "RETURN",
            "FUNC_BEGIN",
            "FUNC_END",
            "SEQ_BEGIN",
            "SEQ_END",
            "PAR_BEGIN",
            "PAR_END",
            "THREAD_START",
            "THREAD_END",
        ):
            if self.arg1 is not None:
                return f"{self.op} {self.arg1}"
            return self.op
        if self.op in ("IF_FALSE", "IF_TRUE"):
            return f"{self.op} {self.arg1} GOTO {self.result}"
        if self.op == "ASSIGN":
            return f"{self.result} = {self.arg1}"
        if self.op == "UNARY":
            return f"{self.result} = {self.arg1} {self.arg2}"
        if self.arg2 is None:
            return f"{self.result} = {self.arg1}"
        return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
