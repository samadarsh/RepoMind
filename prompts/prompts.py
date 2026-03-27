from langchain_core.prompts import PromptTemplate

# -------------------------------------------------------------------
# CLASSIFIER PROMPT
# -------------------------------------------------------------------

CLASSIFIER_PROMPT = PromptTemplate.from_template(
    """
    ### REPOSITORY NAME: {repo_name}
    
    ### README CONTENT (IF ANY):
    {readme_content}
    
    ### REPOSITORY FILE LIST:
    {file_list}
    
    ### INSTRUCTION:
    You are an expert Software Architect identifying the nature of a GitHub repository.
    Based on the repository name, file list, and README content provided, classify this project into ONE of the following types:
    - Portfolio Website
    - Machine Learning Project
    - Web Application
    - Library/SDK
    - Script Collection
    - Data Science Notebook
    - Backend API
    - Unknown

    Output ONLY a valid JSON object with standard double quotes matching this exact structure:
    {{
        "type": "The Exact Classification String",
        "reason": "A 1-2 sentence explanation of why it fits this classification based on the files/README."
    }}
    
    Ensure your response contains NO markdown formatting wrappers and NO additional text.
    """
)

# -------------------------------------------------------------------
# ANALYZER PROMPT
# -------------------------------------------------------------------

ANALYZER_PROMPT = PromptTemplate.from_template(
    """
    ### REPOSITORY FILE LIST:
    {file_list}

    ### INSTRUCTION:
    The above list contains files from a GitHub repository.

    Your job is to analyze the repository like a senior software engineer and identify the most important files.

    Focus on:
    - Entry point files (main.py, app.py, index.py)
    - Core logic files and Data Science Notebooks (.ipynb)
    - Files responsible for main functionality
    - Critical documentation (README.md) if it explains workflow

    Ignore:
    - Config files
    - Minor helper files
    - Static assets
    - Setup files (setup.py, requirements.txt, etc.)

    ### OUTPUT FORMAT:
    Return ONLY valid JSON:

    {{
        "important_files": [
            "file_path_1",
            "file_path_2"
        ]
    }}

    ### RULES:
    - Do NOT include explanations
    - Do NOT include extra text
    - Do NOT include markdown
    - Ensure valid JSON (no trailing commas)

    ### VALID JSON (NO PREAMBLE):
    """
)

# -------------------------------------------------------------------
# MAP STEP PROMPT
# -------------------------------------------------------------------

MAP_STEP_PROMPT = PromptTemplate.from_template(
    """
    ### REPOSITORY CONTEXT:
    Name: {repo_name}
    Classification: {repo_class}

    ### FILE PATH:
    {file_path}

    ### FILE CONTENT:
    {file_content}

    ### INSTRUCTION:
    You are a senior technical writer explaining a single file within the broader context of the `{repo_name}` project (categorized as a {repo_class}).

    WARNING: Do NOT infer or assume the entire repository's fundamental purpose based on this single file. Explain ONLY what this file contributes to the broader ecosystem.

    Please provide a clear, concise, and structured explanation of:
    1. **Purpose**: What is the specific goal of this file within the {repo_class}?
    2. **Core Components**: What are the primary functions, classes, or logic blocks within this file and what do they do?
    3. **Role in Project**: How does this file fit into the broader project architecture context?

    Keep your explanation readable and professional. Avoid overly verbose descriptions. You may use bullet points and bold text for clarity.

    ### EXPLANATION:
    """
)

# -------------------------------------------------------------------
# AGGREGATOR PROMPT
# -------------------------------------------------------------------

AGGREGATOR_PROMPT = PromptTemplate.from_template(
    """
    ### PROJECT CONTEXT
    Repository Name: {repo_name}
    Classification: {repo_class}

    ### ORIGINAL README CONTENT (IF ANY):
    {readme_content}

    ### INDIVIDUAL FILE EXPLANATIONS:
    {file_summaries}

    ### INSTRUCTION:
    You are an expert Software Architect and Technical Writer analyzing a GitHub repository.

    You are provided with structured summaries of the repository’s code files. The repository may be:
    - A full application
    - A machine learning project
    - A collection of scripts
    - A notebook-based workflow
    - Or unstructured/raw code files

    Your task is to generate a clear, professional, and structured technical overview based ONLY on the provided summaries.

    Do NOT assume the repository is a complete product. Adapt your explanation based on what actually exists in the codebase.

    Maintain a highly technical and professional tone. Do not use emojis. Do not include markdown code block wrappers (like ```markdown). Output only clean formatted text.

    ---

    ### RULES:

    - Always strictly follow the section structure below.
    - Include all MANDATORY sections.
    - Include OPTIONAL sections ONLY if they are relevant to the repository.
    - If a section is not applicable (e.g., no clear architecture, no real-world application, or minimal logic), OMIT that section completely.
    - Do NOT invent details that are not present in the code summaries.
    - Avoid generic statements like “uses popular libraries” unless they are directly relevant.
    - Be specific whenever possible (e.g., mention actual transformations, logic, or model types if known).

    ---

    ## GitHub Repo Overview
    [MANDATORY: Provide a clear, factual description of what exists in the repository. If it is not a complete project, describe it as a codebase, collection of scripts, or experimental work accordingly.]

    ⸻

    ## What the Repository Does
    [MANDATORY: Bullet points explaining the actual functionality, logic, and outputs derived from the code.]

    ⸻

    ## Core Workflow
    [OPTIONAL: Include ONLY if there is a clear logical flow (e.g., Input → Processing → Output). Skip if the repo is loosely structured.]

    ⸻

    ## Architecture Breakdown
    [OPTIONAL: Include ONLY if there are clearly defined modules/files with distinct responsibilities.]

    ⸻

    ## Key Features
    [MANDATORY: Identify 2–4 concrete technical features based on actual implementation.]

    ⸻

    ## Strengths of the Repository
    [OPTIONAL: Include ONLY if meaningful strengths can be inferred from structure, clarity, or implementation.]

    ⸻

    ## Areas for Improvement
    [OPTIONAL: Provide 2–4 realistic and actionable technical improvements.]

    ⸻

    ## Advanced Upgrades
    [OPTIONAL: Suggest 1–3 high-value enhancements ONLY if the repository has scope for extension.]

    ⸻

    ## Real-World Applications
    [OPTIONAL: Include ONLY if the repository has clear practical use cases.]

    ⸻

    ## Tech Concepts Demonstrated
    [OPTIONAL: List actual technical concepts, patterns, or tools used.]

    ⸻

    ## One-Line Summary
    [MANDATORY: Provide a concise, single-sentence technical summary of the repository. Do NOT add any headings after this.]
    """
)
