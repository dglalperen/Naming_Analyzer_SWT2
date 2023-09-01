import ast
import os
from utils import get_repo
import re

def analyze_code(file_path):
    try:
        with open(file_path, "r") as source:
            code_str = source.read()
            tree = ast.parse(code_str)
    except SyntaxError:
        # Versuchen Sie, Python 2-spezifische Konstrukte anzupassen
        modified_code_str = code_str.replace("print ", "print(") + ")"
        try:
            tree = ast.parse(modified_code_str)
        except:
            # Wenn der Code weiterhin nicht geparst werden kann, geben Sie ein leeres Dict zurück
            return {
                "function": [],
                "class": [],
                "variable": [],
                "constant": []
            }

    function_names = set()
    class_names = set()
    constant_names = set()
    variable_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not (node.name.startswith('__') and node.name.endswith('__')):
            function_names.add(node.name)
        elif isinstance(node, ast.ClassDef):
            class_names.add(node.name)
        elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id.isupper():
                constant_names.add(node.targets[0].id)
            elif not (node.targets[0].id.startswith('__') and node.targets[0].id.endswith('__')):
                variable_names.add(node.targets[0].id)

    variable_names -= constant_names  # Remove names that are in both variable and constant sets

    return {
        "function": list(function_names),
        "class": list(class_names),
        "variable": list(variable_names),
        "constant": list(constant_names)
    }

def summarize_results(results):
    summary = {"function": [], "class": [], "variable": [], "constant": []}

    for result in results:
        for key in result:
            summary[key] += [item for item in result[key] if item not in summary[key] and item != '__init__']

    return summary


def analyze_repository(repo_name):
    results = []

    repo_url = f'https://github.com/{repo_name}'

    # Define repo directory
    repo_dir = os.path.abspath(f'./repos/{repo_name}')

    # Check if repo_dir exists, if not clone the repo
    if not os.path.exists(repo_dir):
        if repo_url:
            print(f"Repo {repo_name} does not exist, cloning it now.")
            get_repo(repo_url)
        else:
            print(f"Repo {repo_name} does not exist and no repoURL provided to clone.")
            return []

    # Navigate through the cloned directory
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
