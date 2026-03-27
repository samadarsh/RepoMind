from git import Repo
import os

def clone_repo(repo_url, repo_path="repo"):
    """
    Clones a GitHub repository if not already present
    """
    if os.path.exists(repo_path):
        print("Repo already exists. Skipping clone.")
        return repo_path

    print("Cloning repository...")
    Repo.clone_from(repo_url, repo_path)
    print("Cloned successfully!")

    return repo_path

# GET ALL FILES

def get_all_files(repo_path):
    """
    Walk through repo and collect all file paths
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