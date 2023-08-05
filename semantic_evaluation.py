import json
import re
import openai
import logging

OPEN_API_TOKEN = "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"
OPEN_API_TOKEN_WITH_GPT4 = "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"

def ask_chatgpt(text_chunk, api_key):
    openai.api_key = api_key

    prompt = """
    Title: Advanced Python Source Code Naming Analysis
    Prompt:
    As a highly trained AI model developed by OpenAI, your task is to conduct an in-depth analysis of the naming conventions used in a given Python source code. The aim is to evaluate the quality, appropriateness, and consistency of the names used for functions (excluding `__init__` and other dunder methods), classes, and variables (excluding loop iterators like `i` and `j`).

    In this analysis, consider the following criteria:
    - **Descriptiveness**: The names should be descriptive and relevant to their associated code. For example, a function meant to calculate an average could be named 'calculate_average', while 'calc_avg' might be somewhat less clear, and 'function1' would be vague and misleading.
    - **Length**: Very short names (like 'a' or 'x') may not provide enough information about what they represent, while very long names can be cumbersome and may be a sign of trying to do too much with a single variable or function.
    - **Common Misuses**: Names consisting of generic terms (like 'data', 'value') or Python reserved words should be avoided unless their usage is universally understood in the context of programming.
    - **Consistency**: Check for consistency in naming conventions across the codebase. A name might be semantically correct in isolation but if it's not consistent with the rest of the codebase, it can be confusing for others reading the code.
    - **Domain-Specific Conventions**: Depending on the purpose of the program, there may be specific naming conventions or practices that should be followed.

    Your analysis results should be formatted as a JSON object, following this schema:
    {
        "score": "<score>"
    }
    Here, `<score>` represents the calculated score between 0 and 1, expressed as a decimal number in string format. This score should reflect the overall quality of naming in the codebase, taking into account the factors mentioned above. It is the value of the "score" key in the provided JSON schema.
    """
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text_chunk},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4", messages=messages, temperature=0.1
    )

    message = response["choices"][0]["message"]["content"]
    # Extract the numeric score from the AI's message
    score_json = extract_json_from_string(message)

    # Log the chunk of code and the score JSON
    print(f"Chunk: {text_chunk}")
    print(f"Score JSON: {score_json}")

    if score_json is None or 'score' not in score_json:
        print(f'Could not calculate score for chunk: {text_chunk}')
        return {'score': '0'}

    return score_json


def request_code_improvement(code_snippet):
    messages = [
        {
            "role": "system",
            "content": """
    Title: Advanced Python Source Code Semantic Correction

    Prompt:
    As a highly trained AI model developed by OpenAI, your task is to analyze a given Python source code and provide corrections to enhance the semantic appropriateness. The goal is to improve the quality, suitability, and consistency of the names used for functions (excluding `__init__` and other dunder methods), classes, and variables (excluding loop iterators like `i` and `j`).

    In your analysis and correction, consider the following criteria:

    - **Descriptiveness**: The names should be descriptive and relevant to their associated code. If the current names are not clear or misleading, propose better alternatives that convey the purpose of the code more accurately. For example, a function meant to calculate an average could be named 'calculate_average', while 'calc_avg' might be somewhat less clear, and 'function1' would be vague and misleading.

    - **Length**: Very short names (like 'a' or 'x') may not provide enough information about what they represent, while very long names can be cumbersome and may be a sign of trying to do too much with a single variable or function. Provide suggestions to make the names more concise and meaningful.

    - **Common Misuses**: Names consisting of generic terms (like 'data', 'value') or Python reserved words should be avoided unless their usage is universally understood in the context of programming. If such names are present in the code, suggest more specific and relevant alternatives.

    - **Consistency**: Check for consistency in naming conventions across the codebase. A name might be semantically correct in isolation but if it's not consistent with the rest of the codebase, it can be confusing for others reading the code. Propose corrections to ensure consistency.

    - **Domain-Specific Conventions**: Depending on the purpose of the program, there may be specific naming conventions or practices that should be followed. Where applicable, adjust the names to align with such conventions.

    Your corrections should be returned in the form of the modified Python source code, with all the proposed naming changes incorporated. Be sure to provide explanations for your changes so the user can understand your reasoning.
    
    """,
        },
        {"role": "user", "content": code_snippet},
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    improved_code = response["choices"][0]["message"]["content"]
    return improved_code

def get_score(data):
    try:
        score = data.get("score")
        # Check if score is a valid float
        if score is not None:
            float(score)
        else:
            score = 'N/A'  # Or some other default value
    except (AttributeError, ValueError):
        score = 'N/A'  # Or some other default value
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
