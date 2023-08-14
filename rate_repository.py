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
    """
    Calculate the average semantic score of a list of Python files.

    Args:
    python_files (list of str): The Python files to score.
    openai_token (str): The OpenAI API token.

    Returns:
    dict: The average semantic score of the Python files.
    """
    total_weighted_score = 0  # The total weighted score for all chunks
    total_names = 0  # The total number of names in all chunks
    unrated_chunks_counter = 0
    unrated_chunks_dir = "./unrated_chunks"

    # Create directory for unrated chunks if it does not exist
    os.makedirs(unrated_chunks_dir, exist_ok=True)

    # Print the start of the process
    print("Starting the rating process for Python files...")

    # Function to count the number of names in a chunk
    def count_names(chunk):
        # This regex captures python variable, function, and class names
        return len(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", chunk))

    # Iterate over all Python files
    for file in python_files:
        print("=" * 40)  # Separator for clarity
        print(f"Processing file: {file}\n")

        try:
            # Read the file content
            with open(file, "r") as f:
                file_content = f.read()

            # Split large files into chunks
            file_chunks = split_into_chunks(file_content, 6000)

            # Print the number of chunks for the current file
            print(f"File {file} has been split into {len(file_chunks)} chunks.\n")

            # Iterate over all chunks in the current file
            for i, chunk in enumerate(file_chunks):
                # Print the chunk being processed and its content
                print(f"Processing chunk {i+1}/{len(file_chunks)}:")
                print("-" * 20)
                print(chunk)
                print("-" * 20 + "\n")

                # Get the number of names in the chunk
                names_count = count_names(chunk)

                # If there are no names, skip this chunk
                if names_count == 0:
                    print("Skipping chunk due to no names.")
                    continue

                # Ask the model for a score for the current chunk
                score_json = ask_chatgpt(chunk, openai_token)
                score = get_score(score_json)

                # Check if the score is a valid number
                try:
                    score_value = float(score)
                    # Update the weighted score and total names count
                    total_weighted_score += score_value * names_count
                    total_names += names_count

                    # Print the score of the chunk
                    print(f"Chunk score: {score_value}\n")

                except ValueError:
                    # Print an error if the score is not a valid number
                    print(f'Invalid score "{score}" for file: {file}')
                    unrated_chunks_counter += 1
                    with open(
                        f"{unrated_chunks_dir}/_chunk_{unrated_chunks_counter}.py", "w"
                    ) as unrated_file:
                        unrated_file.write(chunk)

        except Exception as e:
            # Print any other errors that occur during processing
            print(f"Error processing file {file}: {e}")

    # Calculate the average score
    average_score = total_weighted_score / total_names if total_names > 0 else 0

    # Print the completion of the process
    print(f"\nRating process completed. Average score: {average_score}")

    # Return the average score as a string in a dictionary
    return {"score": str(average_score)}
