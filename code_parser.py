import ast
from typing import List, Dict, Any


def parse_python_code(code: str) -> Dict[str, Any]:
    tree = ast.parse(code)

    function_list = []
    classes_list = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_info = {"name": node.name,
                         "params": [arg.arg for arg in node.args.args],
                         "docstring": ast.get_docstring(node)}
            function_list.append(func_info)

        elif isinstance(node, ast.ClassDef):
            classes_info = {"name": node.name,
                            "docstring": ast.get_docstring(node),
                            "methods": []}

            for method in node.body:
                if isinstance(method, ast.FunctionDef):
                    method_info = {"name": method.name,
                                   "params": [arg.arg for arg in method.args.args],
                                   "docstring": ast.get_docstring(method)}
                    classes_info["methods"].append(method_info)

            classes_list.append(classes_info)

    return {"functions": function_list,
            "classes": classes_list,
            "total_functions": len(function_list),
            "total_classes": len(classes_list)}
