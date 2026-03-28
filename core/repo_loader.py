from git import Repo, GitCommandError
import os
import re
import tempfile
import logging
from logging.handlers import RotatingFileHandler

# Configure logging with rotation (5MB max, 3 backups)
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("repomind")
if not logger.handlers:
    handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def validate_github_url(url: str) -> bool:
    """
    Validates that the input is a properly formatted GitHub repository URL.
    Accepts HTTPS GitHub URLs with at least a user and repo name.
    """
    pattern = r'^https?://github\.com/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+'
    return bool(re.match(pattern, url.strip()))


def _extract_repo_identifier(url: str) -> str:
    """Extracts 'user/repo' from a GitHub URL for safe logging (no full URL in logs)."""
    try:
        parts = url.strip().rstrip('/').split('github.com/')[-1]
        return parts.split('?')[0].rstrip('.git')
    except Exception:
        return "unknown/repo"


def clone_repo(repo_url):
    """
    Clones a GitHub repository into a unique temporary directory.
    Each call creates a fresh, isolated clone — no folder conflicts possible.
    Returns the path to the cloned repository.
    Raises RuntimeError with a meaningful message if cloning fails.
    """
    repo_id = _extract_repo_identifier(repo_url)

    # Validate URL before attempting clone
    if not validate_github_url(repo_url):
        logger.error(f"Invalid GitHub URL received for: {repo_id}")
        raise ValueError(
            f"Invalid GitHub URL: '{repo_url}'. "
            f"Please provide a valid URL (e.g. https://github.com/user/repo)."
        )

    # Create a unique temporary directory for this clone
    repo_path = tempfile.mkdtemp(prefix="repomind_")

    logger.info(f"Clone started: {repo_id}")
    print(f"📁 Created temp directory: {repo_path}")
    print(f"🔄 Cloning repository: {repo_url}")

    try:
        Repo.clone_from(repo_url, repo_path, multi_options=["--depth=1"])
        logger.info(f"Clone successful: {repo_id}")
        print("✅ Cloned successfully!")
        return repo_path

    except GitCommandError as e:
        logger.error(f"Git clone failed for {repo_id}: {str(e)}")
        raise RuntimeError(
            f"Git clone failed for '{repo_url}'. "
            f"Please check the URL is correct and the repository is public.\n"
            f"Details: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error cloning {repo_id}: {str(e)}")
        raise RuntimeError(
            f"Unexpected error while cloning '{repo_url}'.\n"
            f"Details: {str(e)}"
        )


def get_all_files(repo_path):
    """
    Walk through repo and collect all file paths.
    """
    file_paths = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)

    return file_paths


# Print Structure (for debugging)

def print_sample_files(file_paths, limit=10):
    print("\nSample files:")
    for file in file_paths[:limit]:
        print(file)


# testing

if __name__ == "__main__":
    repo_url = "https://github.com/samadarsh/GenAI-Email-Generator"  # test repo
    
    path = clone_repo(repo_url)
    files = get_all_files(path)
    
    print(f"\nTotal files: {len(files)}")
    print_sample_files(files)