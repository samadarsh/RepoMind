# RepoMind Global Configuration Files

# The AI Model Name (For Groq)
MODEL_NAME = "openai/gpt-oss-120b"

# Maximum number of files the analyzer will review at once
# We purposefully use 200 instead of 20 to ensure deep codebases are properly scanned.
MAX_FILES = 200

# Groq's free tier allows 8,000 tokens a minute per model, and no single
# request may be larger. These caps keep every call under that limit.

# Files explained in the map step (the analyzer lists the most important first)
MAX_IMPORTANT_FILES = 10
# Characters of each file sent to the map step
MAP_MAX_CHARS = 6000
# Characters of each file explanation passed to the final overview
SUMMARY_MAX_CHARS = 900
# Characters of the README given to the classifier and the final overview
README_MAX_CHARS = 4000
# Paths listed to the classifier
CLASSIFIER_MAX_FILES = 150
# Retries per LLM call when Groq reports a rate limit
MAX_RETRIES = 6
