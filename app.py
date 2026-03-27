import streamlit as st
import os
from chain import RepoExplainerChain

# Set Streamlit page config
st.set_page_config(page_title="RepoMind", page_icon="🤖", layout="wide")

def create_streamlit_app():
    # Application Title and description
    st.title("🤖 RepoMind")
    
    url_input = st.text_input("Enter a GitHub Repository URL:")
    submit_button = st.button("Generate Explanation")

    if submit_button:
        if not url_input.strip():
            st.warning("Please enter a valid GitHub URL.")
            return

        # Simple validation just to check if it's GitHub
        if "github.com" not in url_input.lower():
            st.error("Please provide a valid GitHub repository URL (e.g. https://github.com/user/repo).")
            return

        try:
            with st.spinner("Analyzing repository... This involves fetching the code, identifying key files, and generating explanations. Please wait."):
                
                # Initialize our backend map-reduce chain
                explainer = RepoExplainerChain()

                # Process the URL and retrieve the entire markdown payload
                final_overview_markdown = explainer.process_repository(url_input)
            
            # Display Success and output
            st.success("✅ Analysis Complete!")
            
            st.markdown("---")
            st.markdown(final_overview_markdown)

        except Exception as e:
            st.error(f"An Error Occurred during analysis: {e}")

if __name__ == "__main__":
    create_streamlit_app()
