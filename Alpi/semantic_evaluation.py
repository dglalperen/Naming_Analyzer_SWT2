import re
import openai

OPEN_API_TOKEN = "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"
openai.api_key = OPEN_API_TOKEN


def ask_chatgpt(file_path):
    # Read the file content
    with open(file_path, 'r') as file:
        code_snippet = file.read()

    messages = [
        {"role": "system",
         "content": "You are an AI language model, and your task is to evaluate Python source code concerning the semantic correctness of function, class and variable names. You will return a metric score between 0 and 1 where 1 is perfect."},
        {"role": "user", "content": code_snippet}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    message = response['choices'][0]['message']['content']

    # Extract the numeric score from the AI's message
    score_match = re.search(r"([0-1](\.\d+)?)", message)
    if score_match:
        return float(score_match.group(1))
    else:
        return None

def request_code_improvement(code_snippet):
    messages = [
        {"role": "system",
         "content": "You are an AI language model, and your task is to improve the given Python source code by refactoring function, class, and variable names to enhance their semantic correctness."
        },
        {"role": "user",
         "content": code_snippet
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    improved_code = response['choices'][0]['message']['content']
    return improved_code

