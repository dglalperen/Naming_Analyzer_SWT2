'''

def fork_and_analyze_repositories(df, language):
    # Authenticate with the GitHub API
    github = Github(GITHUB_TOKEN)

    # Get the authenticated user
    user = github.get_user()

    # Fork and clone the repositories from the DataFrame
    forked_repos = []
    all_results = []
    for index, row in df.iterrows():
        repo_url = row["Repository URL"]
        repo_owner, repo_name = repo_url.split("/")[-2:]

        # Fork the repository
        try:
            original_repo = github.get_repo(f"{repo_owner}/{repo_name}")
            forked_repo = user.create_fork(original_repo)
            forked_repos.append(forked_repo)
            print(f"Forked repository: {forked_repo.html_url}")
        except Exception as e:
            print(f"Error forking repository: {repo_url} - {str(e)}")
            continue

        # Clone the forked repository
        os.system(f"git clone {forked_repo.ssh_url}")

        # Change the working directory to the cloned repository
        os.chdir(repo_name)

        # Run SonarCloud analysis
        os.system(f"sonar-scanner -Dsonar.projectKey={user.login}_{repo_name} -Dsonar.sources=. -Dsonar.host.url=https://sonarcloud.io -Dsonar.login={SONAR_TOKEN} -Dsonar.organization={SONAR_ORGANIZATION}")

        # Fetch SonarCloud analysis results
        project_key = f"{user.login}_{repo_name}"
        results = fetch_analysis_results(project_key, SONAR_TOKEN, LANGUAGE_RULES, SONAR_ORGANIZATION)
        all_results.extend(results)

        # Change the working directory back to the parent directory
        os.chdir("..")

        # Remove the cloned repository folder
        os.system(f"rm -rf {repo_name}")

        # Sleep for a while to avoid rate limiting issues
        time.sleep(60)

    return all_results

'''
