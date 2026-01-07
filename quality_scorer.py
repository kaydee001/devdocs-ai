from typing import Dict, List, Any
import re


def score_documentation(parsed_code: Dict[str, Any], generated_docs: str) -> Dict[str, Any]:
    scores = {}
    suggestions = []

    scores["completeness"]
    scores["structure"]
    scores["examples"]
    scores["clarity"]
    scores["coverage"]

    total_score = (scores["completeness"]*0.25 +
                   scores["structure"]*0.2 +
                   scores["examples"]*0.2 +
                   scores["clarity"]*0.2 +
                   scores["coverage"]*0.15)

    suggestions = _generate_suggestions(scores)

    return {"total_score": total_score,
            "breakdown": scores,
            "suggestions": suggestions,
            "grade": _get_grade(total_score)}


def _score_structure(docs: str) -> float:
    score = 0
    docs_lower = docs.lower()

    if "installation" in docs_lower or "install" in docs_lower or "setup" in docs_lower:
        score += 5

    if "usage" in docs_lower:
        score += 5

    if "description" in docs_lower or "overview" in docs_lower:
        score += 5

    if "api" in docs_lower or "reference" in docs_lower:
        score += 5

    return score


def _generate_suggestions(scores: Dict[str, float]) -> List[str]:
    suggestions = []
    if scores["structure"] < 15:
        suggestions.append(
            "Add missing sections : Installation, Usage, Description or API Reference")

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
