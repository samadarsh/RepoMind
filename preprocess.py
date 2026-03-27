import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repo_loader import clone_repo, get_all_files

# 1. Define Ignore Rules

IGNORE_DIRS = [".git", "__pycache__", "venv", "node_modules"]
IGNORE_FILES = [".env", ".gitignore"]
IGNORE_EXT = [".png", ".jpg", ".jpeg", ".gif", ".exe", ".dll", ".csv"]

# 2. Filter Files

def filter_files(file_paths):
    filtered_files = []

    for file in file_paths:
        if any(ignore in file for ignore in IGNORE_DIRS):
            continue
        if any(file.endswith(f) for f in IGNORE_FILES):
            continue
        if any(file.endswith(ext) for ext in IGNORE_EXT):
            continue

        filtered_files.append(file)

    return filtered_files

IMPORTANT_EXT = [".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".go", ".ipynb", ".md"]

def keep_important_files(file_paths):
    return [f for f in file_paths if any(f.endswith(ext) for ext in IMPORTANT_EXT)]

# 4. Read File Content

def read_file(file_path):
    try:
        with open(file_path, "r", errors="ignore") as f:
            return f.read()
    except:
        return ""

# 5. Test It

if __name__ == "__main__":
    repo_url = "https://github.com/samadarsh/GenAI-Email-Generator"

    print("Starting preprocessing...")

    path = clone_repo(repo_url)
    print("Repo path:", path)

    files = get_all_files(path)
    print("Before filtering:", len(files))

    print("\nRaw files:")
    for f in files[:5]:
        print(f)

    files = filter_files(files)
    print("\nAfter filter_files:", len(files))

    files = keep_important_files(files)
    print("After keep_important_files:", len(files))

    print("\nFinal files:")
    for f in files[:10]:
        print(f)
