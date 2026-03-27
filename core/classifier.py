import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from prompts.prompts import CLASSIFIER_PROMPT
from config import MODEL_NAME

class Classifier:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name=MODEL_NAME
        )
        self.parser = JsonOutputParser()

    def classify(self, repo_name: str, file_list: list, readme_content: str) -> str:
        """
        Ingests the fundamental context of a repository and outputs its macro-level classification category.
        """
        print(f"\n🧠 Classifying the intention of repository: {repo_name}...")

        # Cap the file list so we don't blow context windows on massive monorepos
        files_text = "\n".join(file_list[:300])

        # Cap the README to a reasonable length
        readme_text = readme_content[:15000] if readme_content else "No README provided."

        chain = CLASSIFIER_PROMPT | self.llm

        try:
            response = chain.invoke({
                "repo_name": repo_name,
                "file_list": files_text,
                "readme_content": readme_text
            })

            parsed = self.parser.parse(response.content)

            repo_type = parsed.get("type", "Unknown")
            reasoning = parsed.get("reason", "No reason provided.")

            print(f"🎯 Classification Identified: {repo_type}")
            print(f"   Reasoning: {reasoning}\n")

            return repo_type

        except OutputParserException:
            print("⚠️ JSON parsing failed in Classifier. Returning Unknown.")
            return "Unknown"
        except Exception as e:
            print(f"❌ Error in classifier: {str(e)}")
            return "Unknown"
