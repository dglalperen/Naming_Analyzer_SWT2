from semantic_evaluation import ask_chatgpt, get_score
import nltk
from nltk.tokenize import word_tokenize
import os
import re


def split_into_chunks(text, max_chunk_size):
    """
    Split the input text into chunks based on natural breakpoints, such as the end of functions, classes, comments, or multiple newline breaks.

    Args:
    text (str): The input text to split.
    max_chunk_size (int): The desired maximum chunk size.

    Returns:
    list of str: The chunks of the input text.
    """
    # Define split patterns: end of functions/classes, standalone comments, and multi-newlines
    patterns = [
        r"\bdef \b",
        r"\bclass \b",
        r"^\s*#.*$",
        r"(\'\'\'(.?)\'\'\'|\"\"\"(.?)\"\"\")",
        r"\n\s*\n",
    ]

    split_pattern = "|".join(patterns)

    # Split using the patterns but keep the delimiter
    parts = re.split(split_pattern, text, flags=re.MULTILINE | re.DOTALL)
    chunks, chunk = [], ""

    # If no parts are found based on the patterns, treat the entire text as one chunk
    if not parts or len(parts) == 1:
        return [text]

    for part in parts:
        # If adding the next part will exceed the max_chunk_size or if the part matches a pattern
        if len(chunk) + len(part) > max_chunk_size or re.match(
            split_pattern, part, flags=re.MULTILINE | re.DOTALL
        ):
            if chunk:  # if chunk is not empty
                chunks.append(chunk)
                chunk = ""
        chunk += part

    # Add any remaining chunk
    if chunk:
        chunks.append(chunk)

    return chunks


def rate_repository_semantic(python_files, openai_token):
    total_weighted_score = 0
    total_names = 0
    unrated_chunks_counter = 0
    unrated_chunks_dir = "./unrated_chunks"

    os.makedirs(unrated_chunks_dir, exist_ok=True)
    print("Starting the rating process for Python files...")

    # Function to count the number of names in a chunk
    def count_names(chunk):
        return len(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", chunk))

    # Iterate over all Python files
    for file in python_files:
        print("=" * 40)
        print(f"Processing file: {file}\n")

        # Read the file content
        try:
            with open(file, "r") as f:
                file_content = f.read()
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue

        # Split large files into chunks
        file_chunks = split_into_chunks(file_content, 6000)
        print(f"File {file} has been split into {len(file_chunks)} chunks.\n")

        # Process each chunk
        for i, chunk in enumerate(file_chunks):
            names_count = count_names(chunk)
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