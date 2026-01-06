import ast
from typing import TypedDict, Dict, Union, List, Any


class ParseError(TypedDict):
    error: str


class ParseSuccess(TypedDict):
    functions: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    total_functions: int
    total_classes: int


def parse_python_code(code: str) -> Union[ParseError, ParseSuccess]:
    if not code or not code.strip():
        return {"error": "empty code provided"}

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"error": f"invalid python syntax : {str(e)}"}
    except Exception as e:
        return {"error": f"failed to parse code : {str(e)}"}

    function_list = []
    classes_list = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_info = {"name": node.name,
                         "params": [arg.arg for arg in node.args.args],
                         "docstring": ast.get_docstring(node),
                         "return_type": ast.unparse(node.returns) if node.returns else None}
            function_list.append(func_info)

        elif isinstance(node, ast.ClassDef):
            classes_info = {"name": node.name,
                            "docstring": ast.get_docstring(node),
                            "methods": []}

            for method in node.body:
                if isinstance(method, ast.FunctionDef):
                    method_info = {"name": method.name,
                                   "params": [arg.arg for arg in method.args.args],
                                   "docstring": ast.get_docstring(method),
                                   "return_type": ast.unparse(method.returns) if method.returns else None}
                    classes_info["methods"].append(method_info)

            classes_list.append(classes_info)

    return {"functions": function_list,
            "classes": classes_list,
            "total_functions": len(function_list),
            "total_classes": len(classes_list)}
