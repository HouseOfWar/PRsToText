# PRsToText

**A simple tool to fetch GitHub Pull Requests and convert them to digestible text files for stateful agents.**

## 🎯 Purpose

PRsToText is a niche utility designed to help stateful AI agents track project progress by extracting pull request information from GitHub repositories and formatting it into easy-to-read text files. Perfect for keeping your AI assistants up-to-date with the latest changes in your projects.

## 📋 Features

- Fetch the last N pull requests from any GitHub repository
- Supports both public and private repositories (with authentication)
- Outputs formatted text files with PR details including:
  - Title and number
  - State (open, closed, merged)
  - Author
  - URLs
  - Timestamps (created, merged, closed)
- Simple command-line interface
- Respects GitHub API rate limits

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/HouseOfWar/PRsToText.git
cd PRsToText
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up your GitHub token:
```bash
cp .env.example .env
# Edit .env and add your GitHub token
```

## 🔧 Usage

### Basic Usage

1. (Optional) Set up a GitHub Personal Access Token for private repos or higher rate limits:
```bash
export GITHUB_TOKEN="your_github_token_here"
```

2. Run the script with command-line arguments:
```bash
python prs_to_text.py <owner> <repo> [count] [--verbose]
```

Examples:
```bash
# Fetch last 50 PRs from facebook/react
python prs_to_text.py facebook react

# Fetch last 100 PRs from microsoft/vscode
python prs_to_text.py microsoft vscode 100

# Fetch last 250 PRs with complete diffs (verbose mode)
python prs_to_text.py owner repo 250 --verbose

# Verbose mode with short flag
python prs_to_text.py owner repo 500 -v
```

3. Find your output in `{owner}_{repo}_prs.txt`

### Verbose Mode

Use the `--verbose` or `-v` flag to include **complete diffs** for each pull request in the output file. This provides:
- All summary information (title, author, dates, etc.)
- **Complete diff of all changes** made in each PR

**Note:** Verbose mode makes additional API requests (one per PR), so it takes longer and uses more of your API rate limit.

#### Alternative: Environment Variables

You can also use environment variables:
```bash
export REPO_OWNER="facebook"
export REPO_NAME="react"
python prs_to_text.py
```

### Advanced Usage

You can also import and use the functions in your own scripts:

```python
from prs_to_text import get_last_n_pull_requests, write_prs_to_file
import os

token = os.getenv("GITHUB_TOKEN")

# Fetch any number of PRs (automatically handles pagination)
prs = get_last_n_pull_requests("owner", "repo", n=500, token=token)

# Write with verbose mode (includes complete diffs)
write_prs_to_file(prs, "owner", "repo", "my_custom_output.txt", verbose=True, token=token)
```

## 🔑 GitHub Token Setup

To access private repositories or avoid rate limits:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with `repo` scope
3. Set it using one of these methods:

### Option 1: `.env` file (Recommended)
Create a `.env` file in the project directory:
```bash
GITHUB_TOKEN=your_token_here
```

The script will automatically load it!

### Option 2: Environment Variable
Set it as an environment variable:
```bash
export GITHUB_TOKEN="your_token_here"
```

For persistence, add it to your `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export GITHUB_TOKEN="your_token_here"' >> ~/.bashrc
```

## 📊 Output Format

The tool generates a text file with the following format for each PR:

```
Title: Fix bug in authentication module
Number: #42
State: closed
Author: johndoe
URL: https://github.com/owner/repo/pull/42
Created At: 2024-01-15T10:30:00Z
Merged At: 2024-01-16T14:22:00Z
Closed At: 2024-01-16T14:22:00Z
----------------------------------------
```

## 🤖 Use Cases

- **AI Agent Context**: Feed pull request history to stateful AI agents tracking project development
- **Project Summaries**: Quickly review recent changes across repositories
- **Documentation**: Generate change logs or activity reports
- **Onboarding**: Help new team members understand recent project activity

## 📝 Requirements

- Python 3.6+
- `requests` library
- `python-dotenv` library

## 🌐 Documentation

Visit our [GitHub Pages site](https://lmichaelwar.github.io/PRsToText/) for more information.

## 📄 License

This project is open source and available for free use.

## 🤝 Contributing

This is a simple, niche tool, but contributions are welcome! Feel free to open issues or submit pull requests.

## ⚠️ Notes

- Without authentication, you're limited to 60 requests per hour by GitHub's API
- With authentication, the limit increases to 5,000 requests per hour
- The tool automatically handles pagination to fetch any number of PRs (no limit!)
- Each page fetches up to 100 PRs (GitHub API limitation), but the tool will make multiple requests as needed
- Verbose mode makes one additional API request per PR to fetch the complete diff
- The tool includes small delays between requests to be respectful to the GitHub API 
