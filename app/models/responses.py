from typing import Dict, List, Any, Optional
from pydantic import BaseModel


class QualityScore(BaseModel):
    total_score: float
    breakdown: Dict[str, float]
    suggestions: List[str]
    grade: str


class DocumentationMetadata(BaseModel):
    functions_documented: int
    classes_documented: int


class DocumentationResponse(BaseModel):
    readme: str
    metadata: DocumentationMetadata


class FunctionInfo(BaseModel):
    name: str
    params: List[str]
    docstring: Optional[str] = None
    return_type: Optional[str] = None


class ClassInfo(BaseModel):
    name: str
    docstring: Optional[str] = None
    methods: List[FunctionInfo]


class CodeStructure(BaseModel):
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    total_functions: int
    total_classes: int


class ErrorResponse(BaseModel):
    error: str


class AnalysisResponse(BaseModel):
    structure: CodeStructure
    documentation: DocumentationResponse
    quality_score: QualityScore


class PartialAnalysisResponse(BaseModel):
    structure: Optional[CodeStructure] = None
    documentation: Optional[DocumentationResponse] = None
    error: str
