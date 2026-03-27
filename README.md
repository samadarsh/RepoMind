# 🤖 RepoMind

RepoMind is an AI-powered system that takes any GitHub repository link and automatically generates a highly professional, structured architectural overview of its entire codebase. Instead of manually reading every file to understand a project's logic, RepoMind clones the repository locally, filters out noise, and uses a Map-Reduce LLM pipeline to analyze the core code and output a beautiful, structured technical summary.

⸻

## 🧠 What the Project Does

- **Automated Ingestion**: Clones GitHub repositories and extracts files automatically.
- **Smart Filtering**: Ignores massive vendor directories (like `node_modules` or `venv`) and isolates core logic files (`.py, .js, .ts, .ipynb, .md` etc).
- **Intelligent Processing**: Utilizes LangChain and the Groq API (`openai/gpt-oss-120b`) to evaluate the repository.
- **Map-Reduce Architecture**: Splits the analysis. First, it maps individual files, identifying what each specific script does. Then, it reduces those summaries into a cohesive, high-level structural overview.
- **Beautiful Output**: Returns a strictly formatted, professional overview (identifying workflows, tech concepts, key features, and areas for improvement) directly into a minimalist Streamlit interface.

⸻

## ⚙️ Core Architecture Breakdown

1. **`app.py`** - The primary Streamlit frontend and UI entry point.
2. **`chain.py`** - The master controller orchestrating the entire Map-Reduce workflow.
3. **`prompts.py`** - The AI Engine Room containing all distinct, strict LLM instruction templates.
4. **`repo_loader.py` & `preprocess.py`** - Handles `git clone` operations and aggressively filters out non-essential configuration/image files so the AI only reads business logic.
5. **`analyzer.py`** - Identifies the most critical entry-point files among the filtered list.
6. **`map_step.py` & `aggregator.py`** - Invokes the LLM to explain each individual file locally (Map), and then synthesizes them into the final output template (Reduce).

⸻

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ 
- A free [Groq API Key](https://console.groq.com/keys)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/samadarsh/RepoMind.git
cd RepoMind
```

2. **Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Add your API Key**
Create a `.env` file in the root directory and add your Groq key:
```ini
GROQ_API_KEY="gsk_your_api_key_here"
```

### Running the Application

Execute the Streamlit application:
```bash
streamlit run app.py
```
Paste any GitHub repository URL into the interface and watch RepoMind break it down!
