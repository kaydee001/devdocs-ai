from code_parser import parse_python_code
from llm import generate_documentation

test_code = """
def greet(name: str) -> str:
    '''Say hello to someone.'''
    return f"Hello {name}"

class Calculator:
    '''A simple calculator.'''
    def add(self, a: int, b: int) -> int:
        '''Add two numbers.'''
        return a + b
"""
parsed_code = parse_python_code(test_code)
print("parsed structure : ")
print(parsed_code)
print("-"*50)

docs = generate_documentation(parsed_code)
print("generated documentation : ")
print(docs["readme"])
print(f"metadata : {docs["metadata"]}")
