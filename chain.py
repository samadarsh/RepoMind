import os
import shutil

import json

from core.repo_loader import clone_repo, get_all_files
from core.preprocess import filter_files, keep_important_files, extract_readme
from core.analyzer import Analyzer
from core.map_step import MapStep
from core.aggregator import Aggregator
from core.classifier import Classifier

class RepoExplainerChain:
    def __init__(self):
        """
        Initializes the individual components of the explainer pipeline.
        """
        self.analyzer = Analyzer()
        self.mapper = MapStep()
        self.aggregator = Aggregator()
        self.classifier = Classifier()

    def process_repository(self, repo_url: str) -> str:
        """
        Executes the full end-to-end map-reduce pipeline on a GitHub URL.
        Returns the final overview Markdown.
        """
        repo_name = repo_url.rstrip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]

        repo_path = "repo"
        
        # In a web app, users might submit different repos.
        # We clean up any previously cloned repository to ensure a fresh clone.
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        # 1. Clone & Load
        path = clone_repo(repo_url, repo_path)
        files = get_all_files(path)
        
        # 2. Extract Top-Level Context
        readme_content = extract_readme(path)
        
        # 3. Classify the Repository
        repo_class = self.classifier.classify(repo_name, files, readme_content)

        # 4. Filter Noise
        files = filter_files(files)
        files = keep_important_files(files)

        if not files:
            return "No relevant source files found to analyze."

        # 5. Analyze Importance
        important_files = self.analyzer.extract_important_files(files)
        
        if not important_files:
            return "Could not identify distinct core files to explain."

        # 6. Map Step (File-level context explanations)
        explanations = self.mapper.generate_explanations(important_files, repo_name, repo_class)

        # 7. Aggregator (Final holistic reduction)
        final_report = self.aggregator.generate_overview(explanations, repo_name, repo_class, readme_content)

        # 8. Save outputs per user request
        os.makedirs("outputs/json", exist_ok=True)
        os.makedirs("outputs/markdown", exist_ok=True)
        
        with open("outputs/json/summaries.json", "w", encoding="utf-8") as f:
            json.dump(explanations, f, indent=4)
        with open("outputs/markdown/final_output.txt", "w", encoding="utf-8") as f:
            f.write(final_report)

        return final_report
