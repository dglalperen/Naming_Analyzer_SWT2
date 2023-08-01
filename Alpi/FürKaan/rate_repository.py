import os
import glob
from github import Github
from git import Repo

from ..semantic_evaluation import ask_chatgpt,get_score

# openai token ist bei "semantic evaluation vorhanden"

def rate_repository(repo_link, openai_token):
    # Get repo name from the link
    repo_name = repo_link.split("/")[-1]

    # Initialize Github instance with your token
    g = Github(openai_token)

    # Get repo instance
    repo = g.get_repo(repo_name)

    # Clone the repository
    repo_dir = f'/path/to/clone/directory/{repo_name}'
    Repo.clone_from(repo_link, repo_dir)

    # Find all .py files in the cloned repo
    os.chdir(repo_dir)
    python_files = glob.glob('**/*.py', recursive=True)

    # Initialize total score and file count
    total_score = 0
    file_count = 0

    # Iterate over the Python files and rate them
    for file in python_files:
        file_path = os.path.join(repo_dir, file)
        score_json = ask_chatgpt(file_path, openai_token)
        score = get_score(score_json)
        total_score += float(score)
        file_count += 1

    # Calculate the average score
    average_score = total_score / file_count

    return {"score": str(average_score)}
