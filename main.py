from fastapi import FastAPI
from pydantic import BaseModel
from code_parser import parse_python_code

app = FastAPI(title="DevDocs AI",
              description="Code documentation generator",
              version="0.1.0")


class CodeRequest(BaseModel):
    code: str


@app.get("/health")
def health_check():
    return {"status": "healthy",
            "service": "DevDocs AI",
            "version": "0.1.0"}


@app.get("/")
def read_root():
    return {"message": "Welcome to DevDocs AI",
            "docs": "/docs"}


@app.post("/analyze")
def analyze_code(request: CodeRequest):
    result = parse_python_code(request.code)
    return result
