from fastapi import FastAPI
from pydantic import BaseModel

from minipar_core.translation import generate_python

app = FastAPI(title="ms-codegen-python", version="0.1.0")


class GenerateRequest(BaseModel):
    ast: dict
    symbolTable: dict | None = None
    executionMode: str = "LOCAL"
    target: str = "PYTHON"


class GenerateResponse(BaseModel):
    output: str
    code: str | None = None


@app.get("/health")
def health():
    return {"status": "ok", "service": "ms-codegen-python"}


@app.post("/generate", response_model=GenerateResponse)
def generate(body: GenerateRequest):
    result = generate_python(body.ast)
    return GenerateResponse(output=result.output, code=result.code)
