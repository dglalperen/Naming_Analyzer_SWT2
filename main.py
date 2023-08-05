
from rate_repository import rate_repository_semantic
from repos import check_github_api_credentials
from syntactic_score import rate_repository_syntactic
from repos import clone_repo, delete_repo
import nltk

if __name__ == "__main__":
    GITHUB_API_URL = "https://api.github.com"
    github_token = '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'
    repo_url = 'https://github.com/spy16/pyschemes'
    gpt4_key = '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'
    gpt3_key = "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"

    if github_token is None or repo_url is None or gpt4_key is None or gpt3_key is None:
        print("Please set the necessary environment variables.")
        exit(1)

    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')

    try:
        nltk.data.find('corpora/punkt')
    except LookupError:
        nltk.download('punkt')

    try:
        if check_github_api_credentials(GITHUB_API_URL, github_token):

            python_files = clone_repo(repo_url, github_token)
            repo_name = "/".join(repo_url.split("/")[-2:])

            syntactic_score = rate_repository_syntactic(repo_name)
            print(f'Syntactic Score: {syntactic_score}')

            semantic_score = rate_repository_semantic(python_files, gpt4_key)
            print(f'Semantic Score: {semantic_score}')

            # delete repository
            delete_repo(repo_url)

        else:
            print("Github API credentials are not valid")

    except Exception as e:
        print(f'Error occurred during the execution: {e}')
