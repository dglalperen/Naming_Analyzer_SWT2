import ast
import sys

def analyze_code(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())
    function_names = [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    variable_names = [node.targets[0].id for node in ast.walk(tree) if isinstance(node, ast.Assign)]
    constant_names = [node for node in variable_names if node.isupper()]

    return {
        "function": function_names,
        "class": class_names,
        "variable": variable_names,
        "constant": constant_names
    }


if __name__ == "__main__":

    print(analyze_code("./repos.py"))
