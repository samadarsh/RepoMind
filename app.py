import streamlit as st
import os
import re
import time
from chain import RepoExplainerChain

# Set Streamlit page config
st.set_page_config(page_title="RepoMind", page_icon="🤖", layout="wide")

def is_valid_github_url(url: str) -> bool:
    """Quick client-side validation before hitting the backend."""
    pattern = r'^https?://github\.com/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+'
    return bool(re.match(pattern, url.strip()))

def create_streamlit_app():
    # Application Title and description
    st.title("🤖 RepoMind")
    
    url_input = st.text_input("Enter a GitHub Repository URL:")
    submit_button = st.button("Generate Explanation")

    if submit_button:
        if not url_input.strip():
            st.warning("⚠️ Please enter a GitHub repository URL.")
            return

        if not is_valid_github_url(url_input):
            st.error("❌ Invalid URL. Please provide a valid GitHub repository URL (e.g. https://github.com/user/repo).")
            return

        try:
            start = time.time()

            with st.spinner("🔍 Analyzing repository — cloning, classifying, mapping files, and generating insights. This may take a minute..."):
                
                # Initialize our backend map-reduce chain
                explainer = RepoExplainerChain()

                # Process the URL and retrieve the entire markdown payload
                final_overview_markdown = explainer.process_repository(url_input)
            
            elapsed = round(time.time() - start, 1)

            # Display Success and output
            st.success(f"✅ Analysis Complete! (Finished in {elapsed} seconds)")
            
            st.markdown("---")
            st.markdown(final_overview_markdown)

        except ValueError as e:
            st.error(f"❌ Invalid Input: {e}")
        except RuntimeError as e:
            st.error(f"❌ Repository Error: {e}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred. Please try again.\n\nDetails: {e}")

if __name__ == "__main__":
    create_streamlit_app()
