import urllib
import os
import subprocess
import requests
import tempfile
import shutil
import pandas as pd


# CONSTANTS --> später auslagern in env vars
SONAR_ORGANIZATION = "dglalperen"
SONAR_TOKEN = "debe78c7993526771fbb2e040b98c93333094b48"
GITHUB_TOKEN = "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"
LANGUAGE_RULES = {
        "java": "squid:S00100,squid:S00116,squid:S00117",
        "javascript": "javascript:S100,javascript:S101",
        "python": "python:S1542,python:S100",
        "csharp": "csharpsquid:S100,csharpsquid:S101",
        "php": "php:S116,php:S117",
        "ruby": "ruby:S100,ruby:S101",
    }

def get_repo_name(github_url):
    parsed_url = urllib.parse.urlparse(github_url)
    repo_path = parsed_url.path
    repo_name = repo_path.split('/')[-1]
    return repo_name



def analyze_naming_conventions(input_data, language):
    sonarcloud_url = "https://sonarcloud.io"  # SonarCloud URL

    naming_conventions = []

    if os.path.isfile(input_data):
        # Load CSV file into DataFrame
        df = pd.read_csv(input_data)
    else:
        # Create DataFrame with single GitHub repo URL
        df = pd.DataFrame(data={"Repository URL": [input_data]})

    for index, row in df.iterrows():
        repo_url = row["Repository URL"]
        repo_name = get_repo_name(repo_url)

        # Clone the repository into a temporary folder
        temp_dir = tempfile.mkdtemp()
        subprocess.run(["git", "clone", repo_url, temp_dir], check=True)

        project_key = f"repo_{index}"
        project_name = f"Repo {index}"
        project_version = "1.0"

        # Run the SonarCloud scanner
        subprocess.run([
            'sonar-scanner',
            f'-Dsonar.host.url={sonarcloud_url}',
            f'-Dsonar.login={SONAR_TOKEN}',
            f'-Dsonar.organization={SONAR_ORGANIZATION}',
            f'-Dsonar.projectKey={SONAR_ORGANIZATION}:{os.path.basename(repo_name)}',
            f'-Dsonar.projectBaseDir={temp_dir}',
            f'-Dsonar.language={language}',
            f'-Dsonar.python.xunit.reportPath=sonar-python-report.xml'
        ], cwd=temp_dir, check=True)

        # Retrieve the metrics from SonarCloud
        metrics = "ncloc,functions,classes,comment_lines_density,complexity,violations"
        metrics_url = f"{sonarcloud_url}/api/measures/component?component={project_key}&metricKeys={metrics}"
        response = requests.get(metrics_url, auth=(SONAR_TOKEN, ""))

        if response.status_code == 200:
            measures = response.json()["component"]["measures"]

            # Extract the naming convention metric from the SonarCloud measures
            naming_convention = 0  # You can extract the relevant metric from the measures here
            naming_conventions.append(naming_convention)
        else:
            naming_conventions.append(None)

        # Delete the temporary folder
        shutil.rmtree(temp_dir)

    # Add the naming convention metric to the DataFrame
    df["naming_convention"] = naming_conventions
    df.to_csv("repositories.csv", index=False)


