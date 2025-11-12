import requests
import os
import sys
import argparse
import time
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def get_last_n_pull_requests(owner, repo, n=50, token=None):
    """
    Fetches the last 'n' pull requests for a given repository.
    Handles pagination for requests > 100.
    """
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    
    all_prs = []
    page = 1
    per_page = min(100, n)  # GitHub API max per_page is 100
    
    while len(all_prs) < n:
        remaining_prs = n - len(all_prs)
        current_per_page = min(per_page, remaining_prs)
        
        params = {
            'state': 'all',  # Can be 'open', 'closed', or 'all'
            'per_page': current_per_page,
            'page': page,
            'sort': 'created',
            'direction': 'desc'
        }
        
        try:
            print(f"Fetching page {page} (PRs {len(all_prs)+1}-{len(all_prs)+current_per_page})...")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            batch = response.json()
            if not batch:  # No more PRs available
                break
            
            all_prs.extend(batch)
            
            # If we got fewer PRs than requested, we've reached the end
            if len(batch) < current_per_page:
                break
                
            page += 1
            
            # Be nice to the API - small delay between requests
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None if not all_prs else all_prs
    
    return all_prs[:n]  # Return exactly n PRs

def get_pr_diff(owner, repo, pr_number, token=None):
    """
    Fetches the complete diff for a specific pull request.
    """
    headers = {
        'Accept': 'application/vnd.github.v3.diff'
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching diff for PR #{pr_number}: {e}")
        return None

def write_prs_to_file(prs, owner, repo, filename="pull_requests.txt", verbose=False, token=None):
    """
    Writes the details of pull requests to a text file.
    If verbose is True, includes complete diffs for each PR.
    """
    if not prs:
        print("No pull requests to write.")
        return

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"--- Last {len(prs)} Pull Requests ---\n\n")
        
        for idx, pr in enumerate(prs, 1):
            f.write(f"Title: {pr.get('title')}\n")
            f.write(f"Number: #{pr.get('number')}\n")
            f.write(f"State: {pr.get('state')}\n")
            f.write(f"Author: {pr.get('user', {}).get('login')}\n")
            f.write(f"URL: {pr.get('html_url')}\n")
            f.write(f"Created At: {pr.get('created_at')}\n")
            f.write(f"Merged At: {pr.get('merged_at') or 'N/A'}\n")
            f.write(f"Closed At: {pr.get('closed_at') or 'N/A'}\n")
            
            if verbose:
                f.write("\n" + "=" * 80 + "\n")
                f.write("COMPLETE DIFF:\n")
                f.write("=" * 80 + "\n\n")
                
                print(f"Fetching diff for PR #{pr.get('number')} ({idx}/{len(prs)})...")
                diff = get_pr_diff(owner, repo, pr.get('number'), token)
                
                if diff:
                    f.write(diff)
                    f.write("\n")
                else:
                    f.write("(Diff not available)\n")
                
                f.write("\n" + "=" * 80 + "\n")
                
                # Small delay to avoid rate limiting
                time.sleep(0.3)
            
            f.write("-" * 40 + "\n\n")
    
    print(f"Successfully written {len(prs)} pull requests to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Fetch GitHub Pull Requests and convert them to text files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python prs_to_text.py facebook react 30
  python prs_to_text.py microsoft vscode 150 --verbose
  python prs_to_text.py owner repo 500 -v
        '''
    )
    
    parser.add_argument('owner', nargs='?', help='Repository owner (e.g., "facebook")')
    parser.add_argument('repo', nargs='?', help='Repository name (e.g., "react")')
    parser.add_argument('count', nargs='?', type=int, default=50, 
                        help='Number of PRs to fetch (default: 50, no limit)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Include complete diffs for each PR in the output')
    
    args = parser.parse_args()
    
    # Use command-line arguments or fall back to environment variables
    repo_owner = args.owner or os.getenv("REPO_OWNER", "your-repo-owner")
    repo_name = args.repo or os.getenv("REPO_NAME", "your-repo-name")
    pr_count = args.count
    verbose = args.verbose
    
    if repo_owner == "your-repo-owner" or repo_name == "your-repo-name":
        parser.print_help()
        print("\nOr set REPO_OWNER and REPO_NAME environment variables")
        sys.exit(1)
    
    # Obtain a Personal Access Token from GitHub (Settings -> Developer settings -> Personal access tokens)
    # Ensure it has 'repo' scope for private repositories.
    github_token = os.getenv("GITHUB_TOKEN")  # It is recommended to use environment variables

    if not github_token:
        print("Warning: GITHUB_TOKEN environment variable not set. Limited to public repositories or rate limits may apply.")
        print("For private repos or higher rate limits, please set the GITHUB_TOKEN environment variable.")
        # Alternatively, you can hardcode it for testing, but NOT recommended for production:
        # github_token = "YOUR_PERSONAL_ACCESS_TOKEN"
    
    if verbose:
        print(f"Verbose mode enabled: Will fetch complete diffs for all {pr_count} PRs")
        print("Note: This may take significantly longer and consume more API requests.\n")

    pull_requests = get_last_n_pull_requests(repo_owner, repo_name, n=pr_count, token=github_token)

    if pull_requests:
        write_prs_to_file(pull_requests, repo_owner, repo_name, 
                         f"{repo_owner}_{repo_name}_prs.txt", 
                         verbose=verbose, token=github_token)
    else:
        print("Could not retrieve pull requests.")
