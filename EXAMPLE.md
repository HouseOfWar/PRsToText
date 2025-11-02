# Usage Examples

## Example 1: Fetch PRs from a Public Repository

```python
from prs_to_text import get_last_n_pull_requests, write_prs_to_file

# Fetch last 30 PRs from React repository
prs = get_last_n_pull_requests('facebook', 'react', n=30, token=None)

if prs:
    write_prs_to_file(prs, 'react_recent_prs.txt')
    print(f"Fetched {len(prs)} pull requests from React!")
```

## Example 2: Fetch PRs from a Private Repository

```python
import os
from prs_to_text import get_last_n_pull_requests, write_prs_to_file

# Set your token
token = os.getenv('GITHUB_TOKEN')

# Fetch PRs from your private repo
prs = get_last_n_pull_requests('mycompany', 'private-repo', n=100, token=token)

if prs:
    write_prs_to_file(prs, 'private_repo_prs.txt')
```

## Example 3: Custom Formatting

```python
from prs_to_text import get_last_n_pull_requests

prs = get_last_n_pull_requests('microsoft', 'vscode', n=10, token=None)

if prs:
    with open('custom_output.txt', 'w') as f:
        f.write("# VSCode Recent Pull Requests\n\n")
        for pr in prs:
            f.write(f"- [{pr['title']}]({pr['html_url']}) by @{pr['user']['login']}\n")
```

## Example 4: Filter Only Merged PRs

```python
from prs_to_text import get_last_n_pull_requests, write_prs_to_file

prs = get_last_n_pull_requests('nodejs', 'node', n=100, token=None)

if prs:
    # Filter only merged PRs
    merged_prs = [pr for pr in prs if pr.get('merged_at')]
    write_prs_to_file(merged_prs, 'nodejs_merged_prs.txt')
    print(f"Found {len(merged_prs)} merged PRs out of {len(prs)} total")
```

## Example 5: Command Line with Arguments

Create a simple wrapper script `fetch_prs.py`:

```python
#!/usr/bin/env python3
import sys
import os
from prs_to_text import get_last_n_pull_requests, write_prs_to_file

if len(sys.argv) < 3:
    print("Usage: python fetch_prs.py <owner> <repo> [count]")
    sys.exit(1)

owner = sys.argv[1]
repo = sys.argv[2]
count = int(sys.argv[3]) if len(sys.argv) > 3 else 50

token = os.getenv('GITHUB_TOKEN')
prs = get_last_n_pull_requests(owner, repo, n=count, token=token)

if prs:
    filename = f"{owner}_{repo}_prs.txt"
    write_prs_to_file(prs, filename)
    print(f"✓ Saved {len(prs)} PRs to {filename}")
else:
    print("✗ Failed to fetch PRs")
    sys.exit(1)
```

Usage:
```bash
python fetch_prs.py facebook react 25
python fetch_prs.py microsoft typescript 100
```

## Example 6: Feed to AI Agent

```python
from prs_to_text import get_last_n_pull_requests

# Fetch recent PRs
prs = get_last_n_pull_requests('openai', 'openai-python', n=20, token=None)

if prs:
    # Create a summary for your AI agent
    context = "Recent pull requests in OpenAI Python SDK:\n\n"
    for pr in prs:
        context += f"PR #{pr['number']}: {pr['title']} ({pr['state']})\n"
        context += f"  By {pr['user']['login']} at {pr['created_at']}\n"
        if pr.get('merged_at'):
            context += f"  ✓ Merged at {pr['merged_at']}\n"
        context += "\n"
    
    # Now you can feed this context to your AI agent
    print(context)
```

## Tips

1. **Rate Limits**: Without authentication, GitHub limits you to 60 requests/hour. With a token, you get 5,000 requests/hour.

2. **Pagination**: The GitHub API limits results to 100 per page. To get more than 100 PRs, you'd need to implement pagination.

3. **Token Security**: Never hardcode tokens in your scripts. Always use environment variables or secure credential storage.

4. **Error Handling**: The script handles common errors gracefully, but you may want to add additional error handling for production use.
