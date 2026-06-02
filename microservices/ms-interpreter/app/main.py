from fastapi import FastAPI
from pydantic import BaseModel

from minipar_core.translation import interpret_ast

app = FastAPI(title="ms-interpreter", version="0.2.0")


class ExecuteRequest(BaseModel):
    ast: dict
    symbolTable: dict | None = None
    executionMode: str = "LOCAL"
    target: str = "INTERPRETER"


class ExecuteResponse(BaseModel):
    output: str
    exitCode: int = 0


@app.get("/health")
def health():
    return {"status": "ok", "service": "ms-interpreter"}


@app.post("/execute", response_model=ExecuteResponse)
def execute(body: ExecuteRequest):
    result = interpret_ast(body.ast)
    return ExecuteResponse(output=result.output, exitCode=result.exit_code)
