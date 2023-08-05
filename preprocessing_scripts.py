import ast
from repos import clone_repo, delete_repo
import os
import subprocess
import shutil


def analyze_code(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())
    function_names = [node.name.lower() for node in ast.walk(tree)
                      if isinstance(node, ast.FunctionDef) and not (node.name.startswith('__') and node.name.endswith('__'))]
    class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    constant_names = [node.targets[0].id for node in ast.walk(tree) if
                      isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
                      and node.targets[0].id.isupper()]
    variable_names = [node.targets[0].id for node in ast.walk(tree) if
                      isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
                      and not (node.targets[0].id.startswith('__') and node.targets[0].id.endswith('__'))]
    variable_names = [node for node in variable_names if node not in constant_names]

    return {
        "function": function_names,
        "class": class_names,
        "variable": variable_names,
        "constant": constant_names
    }


def summarize_results(results):
    summary = {"function": [], "class": [], "variable": [], "constant": []}

    for result in results:
        for key in result:
            summary[key] += [item for item in result[key] if item not in summary[key] and item != '__init__']

    return summary


def analyze_repository(repo_name):

    results = []

    # Define repo directory
    repo_dir = os.path.abspath(f'./repos/{repo_name}')

    # Durch das geklonte Verzeichnis navigieren
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    results.append(analyze_code(file_path))
                except Exception as e:
                    print(f"Failed to analyze file {file_path}: {e}")

    return results



if __name__ == "__main__":
    token = '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'
    repo_url = 'https://github.com/donnemartin/system-design-primer'
    print(analyze_repository(repo_url, token))