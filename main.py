from fastapi import FastAPI
from pydantic import BaseModel
from code_parser import parse_python_code
from llm import generate_documentation
from quality_scorer import score_documentation


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
    parsed_code = parse_python_code(request.code)

    if "error" in parsed_code:
        return {"error": parsed_code["error"]}

    docs = generate_documentation(parsed_code)
    if "error" in docs:
        return {
            "structure": parsed_code,
            "error": docs["error"]
        }

    try:
        quality = score_documentation(parsed_code, docs["readme"])
    except Exception as e:
        return {
            "structure": parsed_code,
            "documentation": docs,
            "error": f"Scoring failed : {str(e)}"
        }

    return {
        "structure": parsed_code,
        "documentation": docs,
        "quality_score": quality
    }
