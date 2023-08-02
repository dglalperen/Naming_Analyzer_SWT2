import os
import glob
from github import Github
from git import Repo
from semantic_evaluation import ask_chatgpt, get_score
from repos import clone_repo, delete_repo


# openai token ist bei "semantic evaluation vorhanden"

def rate_repository_sematic(python_files, openai_token):

    # Initialize total score and file count
    total_score = 0
    file_count = 0

    # Iterate over the Python files and rate them
    for file in python_files:
        score_json = ask_chatgpt(file, openai_token)
        score = get_score(score_json)
        total_score += float(score)
        file_count += 1

    # Calculate the average score
    average_score = total_score / file_count

    return {"score": str(average_score)}
