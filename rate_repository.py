from semantic_evaluation import ask_chatgpt, get_score
import nltk
from nltk.tokenize import word_tokenize
import logging
import os



def split_into_chunks(text, chunk_size):
    """
    Split the input text into chunks of approximately the given size.

    Args:
    text (str): The input text to split.
    chunk_size (int): The desired chunk size.

    Returns:
    list of str: The chunks of the input text.
    """
    tokens = word_tokenize(text)
    chunks = []

    for i in range(0, len(tokens), chunk_size):
        chunk = ' '.join(tokens[i:i + chunk_size])
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
    total_score = 0  # The total score for all files
    total_files = 0  # The total number of files scored
    unrated_chunks_counter = 0
    unrated_chunks_dir = "./unrated_chunks"

    # Create directory for unrated chunks if it does not exist
    os.makedirs(unrated_chunks_dir, exist_ok=True)

    # Iterate over all Python files
    for file in python_files:
        try:
            # Log the file being processed
            print(f"Processing file: {file}")

            # Read the file content
            with open(file, "r") as f:
                file_content = f.read()

            # Split large files into chunks of 8000 tokens
            file_chunks = split_into_chunks(file_content, 6000)

            # Iterate over all chunks in the current file
            for i, chunk in enumerate(file_chunks):
                # Log the chunk being processed
                print(f"Processing chunk {i+1}/{len(file_chunks)}")

                # Ask the model for a score for the current chunk
                score_json = ask_chatgpt(chunk, openai_token)
                score = get_score(score_json)

                # Check if the score is a valid number
                try:
                    score_value = float(score)
                    # Add the score to the total and increment the number of files
                    total_score += score_value
                    total_files += 1

                    # Log the score of the chunk
                    print(f"Chunk score: {score_value}")

                except ValueError:
                    # Log an error if the score is not a valid number
                    print(f'Invalid score "{score}" for file: {file}')
                    unrated_chunks_counter += 1
                    with open(f"{unrated_chunks_dir}/_chunk_{unrated_chunks_counter}.py", "w") as unrated_file:
                        unrated_file.write(chunk)

        except Exception as e:
            # Log any other errors that occur during processing
            print(f'Error processing file: {e}')

    # Calculate the average score
    average_score = total_score / total_files if total_files > 0 else 0

    # Return the average score as a string in a dictionary
    return {"score": str(average_score)}

