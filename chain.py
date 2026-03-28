import os
import time

import json
import shutil
import logging

from core.repo_loader import clone_repo, get_all_files
from core.preprocess import filter_files, keep_important_files, extract_readme
from core.analyzer import Analyzer
from core.map_step import MapStep
from core.aggregator import Aggregator
from core.classifier import Classifier

logger = logging.getLogger("repomind")

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
        Each run clones into an isolated temp directory — no folder conflicts.
        Returns the final overview Markdown.
        """
        start_time = time.time()

        repo_name = repo_url.rstrip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]

        # 1. Clone into a unique temp directory
        logger.info(f"Pipeline started for: {repo_name}")
        path = clone_repo(repo_url)
        
        try:
            files = get_all_files(path)
            logger.info(f"[{repo_name}] Total files discovered: {len(files)}")
        
            # 2. Extract Top-Level Context
            readme_content = extract_readme(path)
            logger.info(f"[{repo_name}] README extracted: {'Yes' if readme_content else 'No'}")
            
            # 3. Classify the Repository
            repo_class = self.classifier.classify(repo_name, files, readme_content)
            logger.info(f"[{repo_name}] Classification: {repo_class}")

            # 4. Filter Noise
            files = filter_files(files)
            files = keep_important_files(files)
            logger.info(f"[{repo_name}] Files after filtering: {len(files)}")

            if not files:
                return "No relevant source files found to analyze."

            # 5. Analyze Importance
            important_files = self.analyzer.extract_important_files(files)
            logger.info(f"[{repo_name}] Important files identified: {len(important_files)}")
            
            if not important_files:
                return "Could not identify distinct core files to explain."

            # 6. Map Step (File-level context explanations)
            explanations = self.mapper.generate_explanations(important_files, repo_name, repo_class)
            logger.info(f"[{repo_name}] Files explained: {len(explanations)}")

            # 7. Aggregator (Final holistic reduction)
            final_report = self.aggregator.generate_overview(explanations, repo_name, repo_class, readme_content)

            # 8. Save outputs per user request
            os.makedirs("outputs/json", exist_ok=True)
            os.makedirs("outputs/markdown", exist_ok=True)
            
            with open("outputs/json/summaries.json", "w", encoding="utf-8") as f:
                json.dump(explanations, f, indent=4)
            with open("outputs/markdown/final_output.txt", "w", encoding="utf-8") as f:
                f.write(final_report)

            elapsed = round(time.time() - start_time, 2)
            logger.info(f"[{repo_name}] Pipeline completed in {elapsed}s")
            return final_report

        finally:
            # Always clean up the temp directory after processing
            shutil.rmtree(path, ignore_errors=True)
            logger.info(f"[{repo_name}] Temp directory cleaned up")

