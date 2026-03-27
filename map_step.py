import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

from preprocess import read_file
from prompts import MAP_STEP_PROMPT

# Load environment variables
load_dotenv()


class MapStep:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="openai/gpt-oss-120b"
        )
        self.parser = StrOutputParser()

    def generate_explanations(self, file_paths):
        """
        Iterates over the given file paths, reads their content,
        and uses the LLM to generate an explanation for each file.
        Returns a dictionary mapping file path to its explanation.
        """
        explanations = {}
        chain = MAP_STEP_PROMPT | self.llm | self.parser

        print(f"🧠 Generating explanations for {len(file_paths)} files...")

        for file_path in file_paths:
            print(f"  -> Explaining: {file_path}")
            content = read_file(file_path)

            if not content.strip():
                print(f"     ⚠️ Skipping empty or unreadable file: {file_path}")
                explanations[file_path] = "File is empty or could not be read."
                continue

            try:
                # We cap content to a reasonable length just to prevent exceeding token limits on gigantic files
                max_chars = 30000 
                if len(content) > max_chars:
                    content = content[:max_chars] + "\n... [CONTENT TRUNCATED FOR LENGTH]"

                explanation = chain.invoke({
                    "file_path": file_path,
                    "file_content": content
                })

                explanations[file_path] = explanation

            except Exception as e:
                print(f"     ❌ Error explaining {file_path}: {str(e)}")
                explanations[file_path] = f"Error generating explanation: {str(e)}"

        print("✅ Explanations generated successfully.\n")
        return explanations


# 🧪 TEST BLOCK
if __name__ == "__main__":
    from preprocess import filter_files, keep_important_files
    from repo_loader import clone_repo, get_all_files
    from analyzer import Analyzer

    repo_url = "https://github.com/samadarsh/GenAI-Email-Generator"

    print("🔄 Loading repository...")
    path = clone_repo(repo_url)
    files = get_all_files(path)

    files = filter_files(files)
    files = keep_important_files(files)

    analyzer = Analyzer()
    important_files = analyzer.extract_important_files(files)

    print("\n🔥 Important Files Identified:")
    for f in important_files:
        print(f" - {f}")
    
    print("\n")

    mapper = MapStep()
    explanations = mapper.generate_explanations(important_files)

    print("\n📝 === FINAL EXPLANATIONS ===")
    for path, exp in explanations.items():
        print(f"\n--- {path} ---")
        print(exp)
        print("-" * 40)
