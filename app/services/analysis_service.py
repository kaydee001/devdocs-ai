from typing import Dict, Any
from app.core.code_parser import parse_python_code
from app.core.llm_service import generate_documentation
from app.core.quality_scorer import score_documentation


def analyze_source_code(code: str) -> Dict[str, Any]:
    # print("1. starting analysis")
    parsed_code = parse_python_code(code)
    # print(f"2. parsed code : {parsed_code}")

    if "error" in parsed_code:
        return {"error": parsed_code["error"]}

    # print("3. generating docs")
    docs = generate_documentation(parsed_code)
    # print(f"4. docs generated : {docs}")

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
            "quality_score": f"scoring failed : {str(e)}"
        }

    return {
        "structure": parsed_code,
        "documentation": docs,
        "quality_score": quality
    }
