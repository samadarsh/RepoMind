import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

from prompts import ANALYZER_PROMPT

# Load environment variables
load_dotenv()


class Analyzer:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="openai/gpt-oss-120b"
        )

        self.parser = JsonOutputParser()

    def extract_important_files(self, file_list):
        """
        Uses LLM to identify important files in a repository
        """

        chain = ANALYZER_PROMPT | self.llm

        try:
            response = chain.invoke({
                "file_list": "\n".join(file_list[:200])  # Increased limit so real code files aren't truncated out
            })

            # Debug (optional)
            print("RAW LLM OUTPUT:\n", response.content)

            parsed = self.parser.parse(response.content)

            important_files = parsed.get("important_files", [])

            if not isinstance(important_files, list):
                raise ValueError("Invalid format: important_files is not a list")

            return important_files

        except OutputParserException:
            print("⚠️ JSON parsing failed. Raw output:\n", response.content)
            return []

        except Exception as e:
            print("❌ Error in analyzer:", str(e))
            return []


# 🧪 TEST BLOCK
if __name__ == "__main__":
    from preprocess import filter_files, keep_important_files
    from repo_loader import clone_repo, get_all_files

    repo_url = "https://github.com/samadarsh/GenAI-Email-Generator"

    analyzer = Analyzer()

    print("🔄 Loading repository...")

    path = clone_repo(repo_url)
    files = get_all_files(path)

    print(f"📂 Total files: {len(files)}")

    files = filter_files(files)
    files = keep_important_files(files)

    print(f"🧹 After preprocessing: {len(files)} files")

    important_files = analyzer.extract_important_files(files)

    print("\n🔥 Important Files Identified:\n")
    for f in important_files:
        print(f)