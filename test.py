from code_parser import parse_python_code

test_code = """
class Product:
    '''A product class.'''
    def __init__(self, name):
        self.name = name
    
    def greet(name: str) -> str:
        '''Say hello.'''
        return name

    def add() -> int:
        return 56

def top_level_func() -> str:
    '''A standalone function.'''
    pass
"""

result = parse_python_code(test_code)

if "error" in result:
    print(f"error : {result['error']}")
else:
    print("functions :")
    for func in result["functions"]:
        print(
            f" - {func['name']} : {func['params']}, return type : {func['return_type']}")

    print(f"classes : {result['total_classes']}")
    for cls in result["classes"]:
        print(f"class : {cls['name']}")
        print(f"methods : {len(cls['methods'])}")
        for method in cls["methods"]:
            print(
                f" - {method['name']} : {method['params']}, return type : {method['return_type']}")
