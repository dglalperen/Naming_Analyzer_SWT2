import json
import re
import openai
import logging

OPEN_API_TOKEN = "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"
OPEN_API_TOKEN_WITH_GPT4 = "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"


def ask_chatgpt(text_chunk, api_key, max_retries=3):
    openai.api_key = api_key
    retries = 0
    prompt = """
    Title: Advanced Python Source Code Naming Analysis

    Prompt:
    As a highly trained AI model developed by OpenAI, your task is to conduct an in-depth analysis of the naming conventions used in a given Python source code. 
    The aim is to evaluate the quality, appropriateness, and consistency of the names used for functions (excluding __init__ and other dunder methods), classes, and variables (excluding loop iterators like i and j).

    In this analysis, consider the following criteria:

    Descriptiveness: The names should be descriptive and relevant to their associated code. For example, a function meant to calculate an average could be named 'calculate_average', while 'calc_avg' might be somewhat less clear, and 'function1' would be vague and misleading.
    Length: Very short names (like 'a' or 'x') may not provide enough information about what they represent, while very long names can be cumbersome and may be a sign of trying to do too much with a single variable or function.
    Common Misuses: Names consisting of generic terms (like 'data', 'value') or Python reserved words should be avoided unless their usage is universally understood in the context of programming.
    Consistency: Check for consistency in naming conventions across the codebase. A name might be semantically correct in isolation but if it's not consistent with the rest of the codebase, it can be confusing for others reading the code.
    Abstraction: Avoid overly specific names if a more general naming would be appropriate.
    Clarity: Names should not only be descriptive but also intuitive and easily understood.
    Avoidance of Acronyms: Unless they are widely known or defined throughout the code.
    Domain-Specific Conventions: Depending on the purpose of the program, there may be specific naming conventions or practices that should be followed.
    Your analysis results should be formatted as a JSON object, following this schema:

    {
        "score": "<score>"
    }
Here, <score> represents the calculated score between 0.000 and 1.000 with up to 3 decimal places, expressed as a decimal number in string format with a granularity of 0.01. This score should reflect the overall quality of naming in the codebase, taking into account the factors mentioned above. It is the value of the "score" key in the provided JSON schema. Ensure your evaluation is rigorous and critical to ensure code quality."""

    while retries < max_retries:
        messages = [
            {"role": "system", "content": prompt + text_chunk},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=messages, temperature=0
        )

        message = response["choices"][0]["message"]["content"]
        score_json = extract_json_from_string(message)

        score = get_score(score_json)

        if score == "N/A":
            retries += 1
            print(
                f"Invalid score for chunk: {text_chunk}. Retrying {retries}/{max_retries}..."
            )
        else:
            return score_json

    print(
        f"Could not calculate score for chunk: {text_chunk} after {max_retries} retries."
    )
    return {"score": "0"}


def request_code_improvement(code_snippet, api_key=OPEN_API_TOKEN):
    openai.api_key = api_key
    messages = [
        {
            "role": "system",
            "content": """
    Title: Advanced Python Source Code Semantic and Syntactic Correction

    Prompt:
    As a highly trained AI model developed by OpenAI, your task is to analyze a given Python source code and make corrections to the naming of variables, classes, functions, etc. to improve both semantic appropriateness and syntactic correctness. The goal is to improve the quality, appropriateness, and consistency of the names used for functions (except __init__ and other Dunder methods), classes, and variables (except loop iterators such as i and j), and to ensure that the code conforms to PEP 8 standards.
    
    
    Criteria:
    - Descriptiveness: suggest descriptive and relevant names.
    - Length: provide concise and meaningful names.
    - Common misuses: avoid generic terms and reserved Python words.
    - Consistency: Ensure that naming is consistent throughout the code base.
    - Domain-specific conventions: Adhere to all domain-specific practices.
    - Syntactic correctness: conform to PEP 8 guidelines for Python code.
    
    Your corrections should be returned in the form of the modified Python source code, which includes all suggested naming and syntactic name changes. Do not output any other text besides the code.""",
        },
        {"role": "user", "content": code_snippet},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", messages=messages, temperature=0.1
    )

    improved_code = response["choices"][0]["message"]["content"]
    return improved_code


def get_score(data):
    try:
        score = data.get("score")
        # Check if score is a valid float
        if score is not None:
            float(score)
        else:
            score = "N/A"  # Or some other default value
    except (AttributeError, ValueError):
        score = "N/A"  # Or some other default value
    return score


def extract_json_from_string(s):
    # Find the JSON string using a regex
    json_str = re.search(r"\{.*\}", s, flags=re.DOTALL)

    if json_str:
        # Load the JSON string as a Python dict
        json_obj = json.loads(json_str.group())
        return json_obj
    else:
        return None
