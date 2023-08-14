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
