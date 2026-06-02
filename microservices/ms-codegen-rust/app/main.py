from fastapi import FastAPI
from pydantic import BaseModel

from minipar_core.translation import generate_rust

app = FastAPI(title="ms-codegen-rust", version="0.2.0")


class GenerateRequest(BaseModel):
    ast: dict
    symbolTable: dict | None = None
    executionMode: str = "LOCAL"
    target: str = "RUST"


class GenerateResponse(BaseModel):
    output: str
    code: str | None = None


@app.get("/health")
def health():
    return {"status": "ok", "service": "ms-codegen-rust"}


@app.post("/generate", response_model=GenerateResponse)
def generate(body: GenerateRequest):
    result = generate_rust(body.ast)
    return GenerateResponse(output=result.output, code=result.code)
