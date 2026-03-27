import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

from prompts.prompts import AGGREGATOR_PROMPT
import config

# Load environment variables
load_dotenv()


class Aggregator:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name=config.MODEL_NAME
        )
        self.parser = StrOutputParser()

    def generate_overview(self, explanations: dict, repo_name: str, repo_class: str, readme_content: str) -> str:
        """
        Takes a dictionary mapping file paths to their explanations alongside contextual
        repository signals, and generates a cohesive full-repository read.
        """
        if not explanations:
            return "No file explanations provided."

        print("🔄 Aggregating individual summaries into a final overview...")

        # Constructing the context payload
        summaries_text = ""
        for file_path, exp in explanations.items():
            summaries_text += f"\n\n--- FILE: {file_path} ---\n{exp}\n"

        # Capping context size for safety (optional safeguard)
        max_chars = 100000
        if len(summaries_text) > max_chars:
            print("⚠️ Combined text is extremely large! Truncating to prevent token overrun...")
            summaries_text = summaries_text[:max_chars]

        chain = AGGREGATOR_PROMPT | self.llm | self.parser

        try:
            overview = chain.invoke({
                "repo_name": repo_name,
                "repo_class": repo_class,
                "readme_content": readme_content[:15000] if readme_content else "None provided.",
                "file_summaries": summaries_text
            })
            print("✅ Final overview generated successfully!\n")
            return overview
        except Exception as e:
            print(f"❌ Error generating aggregated overview: {str(e)}")
            return f"Error: {str(e)}"


# 🧪 TEST BLOCK: Full Pipeline Check
if __name__ == "__main__":
    from repo_loader import clone_repo, get_all_files
    from preprocess import filter_files, keep_important_files
    from analyzer import Analyzer
    from map_step import MapStep

    repo_url = "https://github.com/samadarsh/GenAI-Email-Generator"

    print("====================================")
    print("🚀 RUNNING FULL ANALYSIS PIPELINE...")
    print("====================================\n")

    # 1. Load Repo
    print("[1/5] Cloning repository...")
    path = clone_repo(repo_url)
    files = get_all_files(path)
    print(f"      Total raw files: {len(files)}")

    # 2. Filter Files
    print("[2/5] Cleaning and filtering codebase...")
    files = filter_files(files)
    files = keep_important_files(files)
    print(f"      Relevant source files: {len(files)}")

    # 3. Analyze Importance
    print("[3/5] Identifying critical components via LLM...")
    analyzer = Analyzer()
    important_files = analyzer.extract_important_files(files)
    print(f"      Selected {len(important_files)} critical files.")

    # 4. Map Step (File level)
    print("[4/5] Explaining individual files...")
    mapper = MapStep()
    explanations = mapper.generate_explanations(important_files)

    # 5. Aggregator (Reduce step)
    print("[5/5] Synthesizing final README report...")
    agg = Aggregator()
    final_report = agg.generate_overview(explanations)

    print("\n--------------------------------")
    print("🌟 FINAL PROJECT README: 🌟")
    print("--------------------------------\n")
    print(final_report)
    print("\n--------------------------------")
