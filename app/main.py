from fastapi import FastAPI, HTTPException, status, UploadFile, File
from pydantic import BaseModel, Field
from app.services.analysis_service import analyze_source_code
from app.models.responses import (
    AnalysisResponse, PartialAnalysisResponse, ErrorResponse)


app = FastAPI(title="DevDocs AI",
              description="Code documentation generator",
              version="0.1.0")


class CodeRequest(BaseModel):
    code: str = Field(..., min_length=1,
                      description="Python source code to analyze")


@app.get("/health")
def health_check():
    return {"status": "healthy",
            "service": "DevDocs AI",
            "version": "0.1.0"}


@app.get("/")
def read_root():
    return {"message": "Welcome to DevDocs AI",
            "docs": "/docs"}


@app.post("/analyze", response_model=AnalysisResponse | PartialAnalysisResponse | ErrorResponse,
          status_code=status.HTTP_200_OK,
          responses={
              200: {"description": "Analysis completed successfully"},
              400: {"model": ErrorResponse, "description": "Invalid python code or empty input"},
              500: {"model": ErrorResponse, "description": "Internal server error"}
          })
def analyze_code(request: CodeRequest):
    try:
        result = analyze_source_code(request.code)

        if "error" in result and "structure" not in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Internal server error : {str(e)}")


@app.post("/analyze/file", response_model=AnalysisResponse | PartialAnalysisResponse | ErrorResponse,
          status_code=status.HTTP_200_OK,
          responses={
              200: {"description": "Analysis completed successfully"},
              400: {"model": ErrorResponse, "description": "Invalid python code or empty input"},
              413: {"model": ErrorResponse, "description": "File too large (max 1 mb)"},
              500: {"model": ErrorResponse, "description": "Internal server error"}
          })
async def analyze_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".py"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid file type, expected .py file, got : {file.filename}")
    try:
        content = await file.read()
        max_size = 1*1024*1024
        if len(content) > max_size:
            raise HTTPException(status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                                detail=f"File too large, max size : 1,b, got {len(content)/1024/1024:.2f} mb")
        code = content.decode("utf-8")

    except UnicodeDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File must be valid UTF-8 encoded text")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to read file : {str(e)}")
    try:
        result = analyze_source_code(code)

        if "error" in result and "structure" not in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Internal server error : {str(e)}")
