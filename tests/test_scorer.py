from code_parser import parse_python_code
from llm import generate_documentation
from quality_scorer import score_documentation

test_code = """
def greet(name: str) -> str:
    '''Say hello.'''
    return f"Hello {name}"

class Calculator:
    '''Simple calculator.'''
    def add(self, a: int, b: int) -> int:
        return a + b
"""

parsed = parse_python_code(test_code)

docs_result = generate_documentation(parsed)

score = score_documentation(parsed, docs_result["readme"])

if "error" in docs_result:
    print("Documentation generation failed")
    exit(1)

print("quality score report : ")
print(f"total score : {score['total_score']}/100 - {score['grade']}")
print(f"breakdown : ")
for category, points in score['breakdown'].items():
    print(f"  {category}: {points:.1f}")
print(f"suggestions : ")
for suggestion in score['suggestions']:
    print(f" - {suggestion}")
