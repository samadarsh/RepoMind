import os
import shutil

import json

from core.repo_loader import clone_repo, get_all_files
from core.preprocess import filter_files, keep_important_files
from core.analyzer import Analyzer
from core.map_step import MapStep
from core.aggregator import Aggregator

class RepoExplainerChain:
    def __init__(self):
        """
        Initializes the individual components of the explainer pipeline.
        """
        self.analyzer = Analyzer()
        self.mapper = MapStep()
        self.aggregator = Aggregator()

    def process_repository(self, repo_url: str) -> str:
        """
        Executes the full end-to-end map-reduce pipeline on a GitHub URL.
        Returns the final overview Markdown.
        """
        repo_path = "repo"
        
        # In a web app, users might submit different repos.
        # We clean up any previously cloned repository to ensure a fresh clone.
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        # 1. Load Repo
        path = clone_repo(repo_url, repo_path=repo_path)
        files = get_all_files(path)

        # 2. Filter out unnecessary docs/images
        files = filter_files(files)
        files = keep_important_files(files)

        if not files:
            return "No relevant source files found to analyze."

        # 3. Analyze for critical files
        important_files = self.analyzer.extract_important_files(files)
        
        if not important_files:
            return "Could not identify distinct core files to explain."

        # 4. Map Phase: Explain individual files
        explanations = self.mapper.generate_explanations(important_files)

        # 5. Reduce Phase: Combine into master overview
        final_report = self.aggregator.generate_overview(explanations)

        # 6. Save outputs per user request
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/summaries.json", "w", encoding="utf-8") as f:
            json.dump(explanations, f, indent=4)
        with open("outputs/final_output.txt", "w", encoding="utf-8") as f:
            f.write(final_report)

        return final_report
