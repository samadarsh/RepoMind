# 🤖 RepoMind

RepoMind is an AI-powered system that takes any GitHub repository link and automatically generates a highly professional, structured architectural overview of its entire codebase. Instead of manually reading every file to understand a project's logic, RepoMind clones the repository locally, filters out noise, classifies the repository type, and uses a context-aware Map-Reduce LLM pipeline to analyze the core code and output a beautiful, structured technical summary.

⸻

## 🧠 What the Project Does

- **Automated Ingestion**: Clones GitHub repositories and extracts files automatically.
- **Smart Filtering**: Ignores massive vendor directories (like `node_modules` or `venv`) and isolates core logic files (`.py, .js, .ts, .ipynb, .md` etc).
- **Context-Aware Classification**: Before analyzing individual files, the system classifies the entire repository (e.g., Portfolio Website, ML Project, Web App, Backend API) using multi-signal reasoning from the repo name, file structure, and README content.
- **Intelligent Processing**: Utilizes LangChain and the Groq API to evaluate the repository with full project context passed into every LLM call.
- **Map-Reduce Architecture**: Splits the analysis. First, it maps individual files with anti-bias guardrails, explaining what each file contributes to the broader project. Then, it reduces those summaries into a cohesive, high-level structural overview.
- **Beautiful Output**: Returns a strictly formatted, professional overview (identifying workflows, tech concepts, key features, and areas for improvement) directly into a minimalist Streamlit interface.

⸻

## 📁 Project Structure

```
RepoMind/
│
├── .env                         # 🔒 Stores your private Groq API Key
├── .gitignore                   # 🛡️ Ignores venv, .env, outputs, logs
├── README.md                    # 📝 Project documentation
├── requirements.txt             # 📦 Dependencies
├── LICENSE                      # 📄 MIT License
├── config.py                    # ⚙️ Centralized settings (model name, limits)
│
├── app.py                       # 🖥️ Streamlit UI (Frontend)
├── chain.py                     # 🧠 Pipeline orchestrator
│
├── core/                        # ⚙️ Core processing engine
│   ├── classifier.py            # 🏷️ Repository type classification
│   ├── analyzer.py              # 🔍 Identifies important files
│   ├── map_step.py              # 📄 File-wise context-aware explanation
│   ├── aggregator.py            # 🧩 Reduce step (final synthesis)
│   ├── preprocess.py            # 🧹 File filtering, cleaning & README extraction
│   ├── repo_loader.py           # 📥 Clone + load repo
│   └── utils.py                 # 🔧 Utility functions
│
├── prompts/                     # 💬 LLM prompt templates
│   └── prompts.py               # All prompt definitions (Classifier, Map, Reduce)
│
├── outputs/                     # 📊 Auto-generated analysis results
│   ├── json/summaries.json      # Individual file explanations
│   └── markdown/final_output.txt# Final aggregated overview
│
└── tests/                       # 🧪 Unit tests
    ├── test_analyzer.py
    ├── test_map_step.py
    └── test_preprocess.py
```

⸻

## ⚙️ Core Architecture Breakdown

### Pipeline Flow
```
URL → Clone → Extract README → Classify Repo → Filter → Analyze → Map (with context) → Aggregate (with context) → Output
```

1. **`app.py`** — The primary Streamlit frontend and UI entry point.
2. **`chain.py`** — The master controller orchestrating the entire pipeline. Extracts the repo name, runs classification, and cascades context through every step.
3. **`core/classifier.py`** — Uses the repo name, file list, and README content to classify the repository type (Portfolio Website, ML Project, Web App, etc.) via structured JSON output.
4. **`core/analyzer.py`** — Identifies the most critical entry-point files among the filtered list.
5. **`core/map_step.py`** — Invokes the LLM to explain each individual file with full repo context and anti-bias guardrails preventing single-file dominance.
6. **`core/aggregator.py`** — Synthesizes all file explanations, repo classification, and README content into the final structured overview.
7. **`core/preprocess.py`** — Handles file filtering, noise removal, and top-level README extraction.
8. **`core/repo_loader.py`** — Handles `git clone` operations and file tree walking.
9. **`prompts/prompts.py`** — The AI Engine Room containing all distinct LLM instruction templates (Classifier, Analyzer, Map Step, Aggregator).
10. **`config.py`** — Centralized configuration for model name and processing limits.

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

