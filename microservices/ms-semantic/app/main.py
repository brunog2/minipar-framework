from fastapi import FastAPI
from pydantic import BaseModel

from minipar_core.semantic_full import analyze_ast_full

app = FastAPI(title="ms-semantic", version="0.3.0")


class AnalyzeRequest(BaseModel):
    ast: dict


class AnalyzeResponse(BaseModel):
    ast: dict
    symbolTable: dict
    errors: list[str] = []


@app.get("/health")
def health():
    return {"status": "ok", "service": "ms-semantic"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(body: AnalyzeRequest):
    ast, symbol_table, errors = analyze_ast_full(body.ast)
    return AnalyzeResponse(ast=ast, symbolTable=symbol_table, errors=errors)
