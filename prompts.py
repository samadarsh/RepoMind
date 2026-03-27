from langchain_core.prompts import PromptTemplate

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
    ### FILE PATH:
    {file_path}

    ### FILE CONTENT:
    {file_content}

    ### INSTRUCTION:
    You are a senior technical writer and software architect. Your job is to explain the file provided above.

    Please provide a clear, concise, and structured explanation of:
    1. **Purpose**: What is the main goal of this file?
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
    ### INDIVIDUAL FILE EXPLANATIONS:
    {file_summaries}

    ### INSTRUCTION:
    You are an expert Software Architect and Technical Writer analyzing a GitHub repository.
    Even if the repository does not have a README file, you have been provided with detailed summaries of its core code files.
    Using ONLY this information, generate a comprehensive, highly professional, structured project overview template.

    Your output MUST strictly follow the exact structure below. Do not use any emojis. Keep the tone highly technical and professional. Do not include markdown code block wrappers (like ```markdown), just plain formatted text.
    
    You must always include the 4 MANDATORY sections. For the OPTIONAL sections, you should only include them if the repository codebase actually warrants it. If an optional section doesn't make sense for a given repository (e.g. it's too simple, has no architecture, or doesn't need strengths listed), omit that section entirely from your output. Do not print the words "(MANDATORY)" or "(OPTIONAL)" in your final output headers.

    ## GitHub Repo Overview
    [MANDATORY: Identify the repository and provide a brief, professional description of its contents and ultimate goal. Do not invent a 'Project Name' if none exists.]

    ⸻

    ## What the Repository Does
    [MANDATORY: Bullet points explaining logic, inputs, and outputs in a clear, professional way]

    ⸻

    ## Core Workflow
    [OPTIONAL: If applicable, provide a simple technical flow (e.g., Input → Processing → Output).]

    ⸻

    ## Architecture Breakdown
    [OPTIONAL: If the repository has a defined architecture, list the critical functional files summarized and give each a bullet point explaining what it handles.]

    ⸻

    ## Key Features
    [MANDATORY: Identify 2-4 key technical features based on the code analysis.]

    ⸻

    ## Strengths of the Repository
    [OPTIONAL: If applicable, list professional bullet points outlining why this codebase is practical, well-structured, or uniquely useful.]

    ⸻

    ## Areas for Improvement
    [OPTIONAL: List 2-4 actionable technical improvements or optimizations that could be added in the future.]

    ⸻

    ## Advanced Upgrades
    [OPTIONAL: If applicable, present 1-3 high-value functional upgrades for scaling or extending the repository.]

    ⸻

    ## Real-World Applications
    [OPTIONAL: If applicable, detail who this repository is for or practical use cases.]

    ⸻

    ## Tech Concepts Demonstrated
    [OPTIONAL: List technical skills, patterns, or frameworks shown in the codebase.]

    ⸻

    ## One-Line Summary
    [MANDATORY: A highly professional, single-sentence technical summary of the entire repository.]

    ### FINAL REPOSITORY OVERVIEW:
    """
)
