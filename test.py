from code_parser import parse_python_code

test_code = """
class Product:
    '''A product class.'''
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        '''Say hello.'''
        return f"Hello from {self.name}"

def top_level_func():
    '''A standalone function.'''
    pass
"""

result = parse_python_code(test_code)

print("functions :")
for func in result["functions"]:
    print(f" - {func['name']} : {func['params']}")

print(f"classes : {result['total_classes']}")
for cls in result["classes"]:
    print(f"class : {cls['name']}")
    print(f"methods : {len(cls['methods'])}")
    for method in cls["methods"]:
        print(f" - {method['name']} : {method['params']}")
