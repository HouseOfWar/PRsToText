import requests
import os
import sys

def get_last_n_pull_requests(owner, repo, n=50, token=None):
    """
    Fetches the last 'n' pull requests for a given repository.
    """
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    params = {
        'state': 'all',  # Can be 'open', 'closed', or 'all'
        'per_page': n,
        'sort': 'created',
        'direction': 'desc'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def write_prs_to_file(prs, filename="pull_requests.txt"):
    """
    Writes the details of pull requests to a text file.
    """
    if not prs:
        print("No pull requests to write.")
        return

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"--- Last {len(prs)} Pull Requests ---\n\n")
        for pr in prs:
            f.write(f"Title: {pr.get('title')}\n")
            f.write(f"Number: #{pr.get('number')}\n")
            f.write(f"State: {pr.get('state')}\n")
            f.write(f"Author: {pr.get('user', {}).get('login')}\n")
            f.write(f"URL: {pr.get('html_url')}\n")
            f.write(f"Created At: {pr.get('created_at')}\n")
            f.write(f"Merged At: {pr.get('merged_at') or 'N/A'}\n")
            f.write(f"Closed At: {pr.get('closed_at') or 'N/A'}\n")
            f.write("-" * 40 + "\n\n")
    print(f"Successfully written {len(prs)} pull requests to {filename}")

if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) >= 3:
        # Usage: python prs_to_text.py <owner> <repo> [count]
        repo_owner = sys.argv[1]
        repo_name = sys.argv[2]
        pr_count = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    else:
        # Default values - replace with your repository details
        repo_owner = os.getenv("REPO_OWNER", "your-repo-owner")  # e.g., "octocat"
        repo_name = os.getenv("REPO_NAME", "your-repo-name")    # e.g., "Spoon-Knife"
        pr_count = 50
        
        if repo_owner == "your-repo-owner" or repo_name == "your-repo-name":
            print("Usage: python prs_to_text.py <owner> <repo> [count]")
            print("Or set REPO_OWNER and REPO_NAME environment variables")
            print("\nExample: python prs_to_text.py facebook react 30")
            sys.exit(1)
    
    # Obtain a Personal Access Token from GitHub (Settings -> Developer settings -> Personal access tokens)
    # Ensure it has 'repo' scope for private repositories.
    github_token = os.getenv("GITHUB_TOKEN") # It is recommended to use environment variables

    if not github_token:
        print("Warning: GITHUB_TOKEN environment variable not set. Limited to public repositories or rate limits may apply.")
        print("For private repos or higher rate limits, please set the GITHUB_TOKEN environment variable.")
        # Alternatively, you can hardcode it for testing, but NOT recommended for production:
        # github_token = "YOUR_PERSONAL_ACCESS_TOKEN" 

    pull_requests = get_last_n_pull_requests(repo_owner, repo_name, n=pr_count, token=github_token)

    if pull_requests:
        write_prs_to_file(pull_requests, f"{repo_owner}_{repo_name}_prs.txt")
    else:
        print("Could not retrieve pull requests.")
