import os
import glob
from github import Github
from git import Repo
from semantic_evaluation import request_code_improvement

def improve_repository(repo_link, openai_token):
    # Get repo name from the link
    repo_name = repo_link.split("/")[-1]

    # Initialize GitHub instance with your token
    g = Github(openai_token)

    # Get repo instance
    repo = g.get_repo(repo_name)

    # Clone the repository
    repo_dir = f'/path/to/clone/directory/{repo_name}'
    Repo.clone_from(repo_link, repo_dir)

    # Find all .py files in the cloned repo
    os.chdir(repo_dir)
    python_files = glob.glob('**/*.py', recursive=True)

    # Create a new directory for improved files
    improved_dir = f'/path/to/improved/directory/{repo_name}'
    os.makedirs(improved_dir, exist_ok=True)

    # Iterate over the Python files and improve them
    for file in python_files:
        file_path = os.path.join(repo_dir, file)
        with open(file_path, 'r') as f:
            code_snippet = f.read()
        improved_code = request_code_improvement(code_snippet, openai_token)

        # Save the improved code in the new directory
        improved_file_path = os.path.join(improved_dir, file)
        with open(improved_file_path, 'w') as f:
            f.write(improved_code)
