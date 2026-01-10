from typing import Dict, List, Any
import re


def score_documentation(parsed_code: Dict[str, Any], generated_docs: str) -> Dict[str, Any]:
    scores = {}
    suggestions = []

    scores["completeness"] = _score_completeness(parsed_code, generated_docs)
    scores["structure"] = _score_structure(generated_docs)
    scores["examples"] = _score_examples(generated_docs)
    scores["clarity"] = _score_clarity(generated_docs)
    scores["coverage"] = _score_coverage(parsed_code, generated_docs)

    total_score = (scores["completeness"]*0.25 +
                   scores["structure"]*0.2 +
                   scores["examples"]*0.2 +
                   scores["clarity"]*0.2 +
                   scores["coverage"]*0.15)

    suggestions = _generate_suggestions(scores)

    return {"total_score": round(total_score, 1),
            "breakdown": scores,
            "suggestions": suggestions,
            "grade": _get_grade(total_score)}


def _score_structure(docs: str) -> float:
    score = 0
    docs_lower = docs.lower()

    if "installation" in docs_lower or "install" in docs_lower or "setup" in docs_lower:
        score += 1

    if "usage" in docs_lower:
        score += 1

    if "description" in docs_lower or "overview" in docs_lower:
        score += 1

    if "api" in docs_lower or "reference" in docs_lower:
        score += 1

    return (score/4) * 100


def _score_completeness(parsed_code: Dict[str, Any], docs: str) -> float:
    score = 0
    docs_lower = docs.lower()

    total_items = 0
    documented_items = 0

    for func in parsed_code.get("functions", []):
        total_items += 1
        if func["name"].lower() in docs_lower:
            documented_items += 1

    for cls in parsed_code.get("classes", []):
        total_items += 1
        if cls["name"].lower() in docs_lower:
            documented_items += 1

    if total_items > 0:
        coverage = documented_items/total_items
        score = coverage*100
    else:
        score = 100

    return score


def _score_examples(docs: str) -> float:
    score = 0

    if "```python" in docs:
        score += 1

    code_block_count = docs.count("```")
    if code_block_count >= 4:
        score += 1

    docs_with_blocks = re.sub(r"```.?```", "", docs, flags=re.DOTALL)

    if "`" in docs_with_blocks:
        score += 1

    return (score/3) * 100


def _score_clarity(docs: str) -> float:
    return 75.0


def _score_coverage(parsed_code: Dict[str, Any], docs: str) -> float:
    return 70.0


def _generate_suggestions(scores: Dict[str, float]) -> List[str]:
    suggestions = []
    if scores["structure"] < 75:
        suggestions.append(
            "Add missing sections : Installation, Usage, Description or API Reference")

    if scores["examples"] < 66:
        suggestions.append(
            "Include code examples showing how to use functions/classes")

    if scores["completeness"] < 80:
        suggestions.append(
            "Document all functions and classes; some are missing from the README")

    if scores["clarity"] < 70:
        suggestions.append(
            "Improve clarity with better descriptions and explainations")

    if scores["coverage"] < 70:
        suggestions.append(
            "Document function paramaters and return values more thoroughly")

    return suggestions


def _get_grade(score: float) -> str:
    if score >= 90:
        return "A : Excellent"
    elif score >= 80:
        return "B : Good"
    elif score >= 70:
        return "C : Fair"
    elif score >= 60:
        return "D : Poor"
    else:
        return "F : Needs work"
