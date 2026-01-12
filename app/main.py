from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from app.services.analysis_service import analyze_source_code
from app.models.responses import (
    AnalysisResponse, PartialAnalysisResponse, ErrorResponse)


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


@app.post("/analyze", response_model=AnalysisResponse | PartialAnalysisResponse | ErrorResponse)
def analyze_code(request: CodeRequest):
    result = analyze_source_code(request.code)

    if "error" in result and "structure" not in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
