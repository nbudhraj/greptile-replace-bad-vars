import os
import requests
import time
import json
import ast
import re
from dotenv import load_dotenv
from urllib.parse import quote

# Load environment variables from a .env file
load_dotenv()

# Retrieve API keys and tokens from environment variables
GREPTILE_API_KEY = os.getenv("GREPTILE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Base URL for Greptile API
BASE_URL = "https://api.greptile.com/v2"

def index_repository(remote, repository, branch):
    """
    Indexes a specified repository on Greptile.

    Args:
        remote (str): The remote service (e.g., "github" or "gitlab").
        repository (str): The repository name in the format <user>/<repo>.
        branch (str): The branch name.

    Returns:
        str: A unique repository ID used to track indexing status.
    """
    # Construct the API endpoint URL
    url = f"{BASE_URL}/repositories"
    
    # Set up the request headers
    headers = {
        "Authorization": f"Bearer {GREPTILE_API_KEY}",
        "X-Github-Token": GITHUB_TOKEN,
        "Content-Type": "application/json"
    }
    
    # Define the data payload for indexing the repository
    data = {
        "remote": remote,
        "repository": repository,
        "branch": branch
    }
    
    # Send a POST request to initiate indexing
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    # Create a unique repository ID for tracking
    repository_id = f"{remote}:{branch}:{repository}"
    
    # Wait until the indexing process is completed
    while True:
        status = check_indexing_status(repository_id)
        if status == "completed":
            break
        time.sleep(30)  # Wait for 30 seconds before checking the status again
    
    return repository_id

def check_indexing_status(repository_id):
    """
    Checks the indexing status of a repository on Greptile.

    Args:
        repository_id (str): The unique ID of the repository.

    Returns:
        str: The current status of the indexing process.
    """
    # Construct the API endpoint URL
    url = f"{BASE_URL}/repositories/{quote(repository_id, safe='')}"
    
    # Set up the request headers
    headers = {
        "Authorization": f"Bearer {GREPTILE_API_KEY}",
        "X-Github-Token": GITHUB_TOKEN
    }
    
    # Send a GET request to check the indexing status
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()["status"]

def get_current_structure(repository_id):
    """
    Retrieves suggestions for improving variable names in the repository.

    Args:
        repository_id (str): The unique ID of the repository.

    Returns:
        str: A JSON string containing an array of tuples with old and new variable names.
    """
    # Construct the API endpoint URL
    url = f"{BASE_URL}/query"
    
    # Set up the request headers
    headers = {
        "Authorization": f"Bearer {GREPTILE_API_KEY}",
        "X-Github-Token": GITHUB_TOKEN,
        "Content-Type": "application/json"
    }
    
    # Define the data payload for the query
    data = {
        "messages": [
            {
                "id": "analysis-1",
                "content": "find all poorly named variables and come up with better names. "
                           "Return just an array of tuples, no additional text: "
                           "(bad variable name, new variable name, filename).",
                "role": "user"
            }
        ],
        "repositories": [
            {
                "remote": repository_id.split(":")[0],
                "repository": repository_id.split(":")[-1],
                "branch": repository_id.split(":")[1]
            }
        ],
        "genius": True,
        "sessionId": "repo-improvement-session"
    }
    
    # Send a POST request to retrieve suggestions
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    return response.text

def generate_replacement_script(replacements):
    """
    Generates a Python script to replace variable names in the repository.

    Args:
        replacements (list): A list of tuples with old and new variable names and filenames.

    Returns:
        str: The generated Python script as a string.
    """
    # Start building the replacement script
    script_lines = [
        "import os\n",
        "import re\n",
        "\n",
        "def apply_replacements():\n",
        "    replacements = [\n"
    ]
    
    # Add each replacement to the script
    for old_var, new_var, filename in replacements:
        if filename[0] == '/':
            filename = filename[1:]  # Remove leading slash from filename if present
        script_lines.append(f"        [\"{old_var}\", \"{new_var}\", \"{filename}\"],\n")
    
    # Continue building the script with logic to apply replacements
    script_lines.extend([
        "    ]\n",
        "    for old_var, new_var, filename in replacements:\n",
        "        if not os.path.isfile(filename):\n",
        "            print(f\"File {filename} does not exist.\")\n",
        "            continue\n",
        "\n",
        "        with open(filename, 'r') as file:\n",
        "            content = file.read()\n",
        "\n",
        "        # Use regex to replace only whole words\n",
        "        new_content = re.sub(rf'\\b{re.escape(old_var)}\\b', new_var, content)\n",
        "\n",
        "        if content != new_content:  # Only write if there are changes\n",
        "            with open(filename, 'w') as file:\n",
        "                file.write(new_content)\n",
        "            print(f\"Replaced '{old_var}' with '{new_var}' in {filename}.\")\n",
        "        else:\n",
        "            print(f\"No replacements needed for {filename}.\")\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    apply_replacements()\n"
    ])
    
    # Combine the script lines into a single string
    script = "".join(script_lines)
    return script

def get_remote_choice():
    """
    Prompts the user to choose between GitHub and GitLab.

    Returns:
        str: "github" if GitHub is chosen, "gitlab" if GitLab is chosen.
    """
    while True:
        remote = input("Pick 1 for Github or 2 for Gitlab: ")
        if remote in ["1", "2"]:
            return "github" if remote == "1" else "gitlab"
        else:
            print("Invalid choice. Please pick 1 for Github or 2 for Gitlab.")

def get_repository():
    """
    Prompts the user to enter the repository name in the correct format.

    Returns:
        str: The repository name entered by the user.
    """
    pattern = r"^[a-zA-Z0-9-]+/[a-zA-Z0-9-_]+$"
    while True:
        repository = input("Enter repo name in the following format <github-user>/<repo-name>: ")
        if re.match(pattern, repository):
            return repository
        else:
            print("Invalid format. Please use the format <github-user>/<repo-name>.")

def get_branch():
    """
    Prompts the user to enter the branch name in the correct format.

    Returns:
        str: The branch name entered by the user.
    """
    pattern = r"^[a-zA-Z0-9-_]+$"
    while True:
        branch = input("Enter branch: ")
        if re.match(pattern, branch):
            return branch
        else:
            print("Invalid branch name. Please use only letters, numbers, hyphens, or underscores.")

def write_replacement_script(filename, script):
    """
    Writes the generated replacement script to a file.

    Args:
        filename (str): The name of the file to write the script to.
        script (str): The script content to be written.
    """
    with open(filename, 'w') as file:
        file.write(script)
    print(f"Replacement script written to {filename}")

def main():
    """
    The main function that orchestrates the entire process of indexing the repository,
    generating replacement suggestions, and writing the replacement script.
    """
    # Gather user inputs
    remote = get_remote_choice()
    repository = get_repository()
    branch = get_branch()
    
    print("Indexing repository...")
    repository_id = index_repository(remote, repository, branch)
    print(repository_id)
    
    print("Finding poorly named variables and coming up with replacement...")
    suggestions = get_current_structure(repository_id)

    vars = json.loads(suggestions)

    # Generate the replacement script based on the suggestions
    script = generate_replacement_script(ast.literal_eval(vars["message"]))

    # Write the replacement script to a file
    write_replacement_script("replace.py", script)

if __name__ == "__main__":
    main()
