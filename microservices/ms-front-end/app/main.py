from fastapi import FastAPI
from pydantic import BaseModel

from minipar_core import parse_source

app = FastAPI(title="ms-front-end", version="0.1.0")


class ParseRequest(BaseModel):
    sourceCode: str


class ParseResponse(BaseModel):
    ast: dict | None = None
    errors: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok", "service": "ms-front-end"}


@app.post("/parse", response_model=ParseResponse)
def parse(body: ParseRequest):
    ast, errors = parse_source(body.sourceCode)
    return ParseResponse(ast=ast, errors=errors)
