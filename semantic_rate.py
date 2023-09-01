from semantic_evaluation import ask_chatgpt, get_score
import os
import re
from nltk.tokenize import word_tokenize
import ast


def get_name_count_from_code_string(code_str):
    try:
        tree = ast.parse(code_str)
    except SyntaxError:
        # Versuchen Sie, Python 2-spezifische Konstrukte anzupassen
        # Hier wird nur das print-Statement berücksichtigt
        # Weitere Anpassungen können hinzugefügt werden, wenn notwendig
        modified_code_str = code_str.replace("print ", "print(") + ")"
        try:
            tree = ast.parse(modified_code_str)
        except:
            return 0

    function_names = [node for node in ast.walk(tree)
                      if isinstance(node, ast.FunctionDef) and not (
                    node.name.startswith('__') and node.name.endswith('__'))]

    class_names = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    assignments = [node for node in ast.walk(tree) if
                   isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)]

    constant_names = [node.targets[0] for node in assignments if node.targets[0].id.isupper()]

    variable_names = [node.targets[0] for node in assignments if
                      not (node.targets[0].id.startswith('__') and node.targets[0].id.endswith('__'))]
    variable_names = [node for node in variable_names if node not in constant_names]

    total_names = len(function_names) + len(class_names) + len(variable_names) + len(constant_names)

    return total_names


def split_into_chunks(text, max_tokens):
    """
    Split the input text into chunks based on natural breakpoints such as the end of functions or classes.
    Chunks the text only if the total tokens exceed max_tokens.

    Args:
    text (str): The input text to split.
    max_tokens (int): The desired maximum number of tokens.

    Returns:
    list of str: The chunks of the input text.
    """

    tokens = word_tokenize(text)
    if len(tokens) <= max_tokens:
        return [text]

    # Splitting points are the end of functions or classes
    splitting_points = [match.end() for match in re.finditer(r"(def|class)\s+\w+\(.*\):", text)]

    chunks, start = [], 0

    for point in splitting_points:
        if start != point:  # Avoids empty chunks
            chunk = text[start:point]
            if len(word_tokenize(chunk)) <= max_tokens:
                chunks.append(chunk)
                start = point

    if start < len(text):
        chunks.append(text[start:])

    return chunks


def rate_repository_semantic(python_files, openai_token):
    total_weighted_score = 0
    total_names = 0
    unrated_chunks_counter = 0
    unrated_chunks_dir = "./unrated_chunks"

    os.makedirs(unrated_chunks_dir, exist_ok=True)
    print("Starting the rating process for Python files...")

    # Iterate over all Python files
    for file in python_files:
        # falls die file eine init datei ist dann soll es übersprungen werden
        if file.endswith("__init__.py"):
            continue

        # Read the file content
        try:
            with open(file, "r") as f:
                file_content = f.read()
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue

        # Split large files into chunks
        file_chunks = split_into_chunks(file_content, 8000)
        #print(f"File {file} has been split into {len(file_chunks)} chunks.\n")

        # Process each chunk
        for chunk in file_chunks:
            names_count = get_name_count_from_code_string(chunk)
            score_json = ask_chatgpt(chunk, openai_token)
            score = get_score(score_json)

            try:
                score_value = float(score)
                total_weighted_score += score_value * names_count
                total_names += names_count
            except ValueError:
                print(f'Invalid score "{score}" for file: {file}')
                unrated_chunks_counter += 1
                with open(
                    f"{unrated_chunks_dir}/_chunk_{unrated_chunks_counter}.py", "w"
                ) as unrated_file:
                    unrated_file.write(chunk)

    average_score = total_weighted_score / total_names if total_names > 0 else 0
    print(f"\nRating process completed. Average score: {average_score}")

    return {"semantic_score": str(average_score)}