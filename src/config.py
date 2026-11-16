"""
Configuration module for the RAG pipeline
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "dados"
VECTOR_STORE_PATH = PROJECT_ROOT / "data" / "vector_store"
MODELS_PATH = PROJECT_ROOT / "models"

# Ensure directories exist
VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
MODELS_PATH.mkdir(parents=True, exist_ok=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# LLM Models
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Embeddings Configuration
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", 
    "paraphrase-multilingual-MiniLM-L12-v2"
)
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "384"))

# Vector Store Configuration
VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "faiss")

# RAG Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))

# Data files
REVIEWS_CSV = DATA_PATH / "reviews_for_rag.csv"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def validate_config():
    """Validate configuration and check for required files"""
    errors = []
    
    # Check if data file exists
    if not REVIEWS_CSV.exists():
        errors.append(f"Reviews CSV not found: {REVIEWS_CSV}")
    
    # Check if at least one API key is configured
    if not any([OPENAI_API_KEY, GROQ_API_KEY, GOOGLE_API_KEY]):
        errors.append(
            "No LLM API key configured. Please set at least one: "
            "OPENAI_API_KEY, GROQ_API_KEY, or GOOGLE_API_KEY"
        )
    
    if errors:
        raise ValueError(
            "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
        )
    
    return True


if __name__ == "__main__":
    print("🔧 Configuration loaded:")
    print(f"  Project Root: {PROJECT_ROOT}")
    print(f"  Data Path: {DATA_PATH}")
    print(f"  Vector Store: {VECTOR_STORE_PATH}")
    print(f"  Embedding Model: {EMBEDDING_MODEL}")
    print(f"  Vector Store Type: {VECTOR_STORE_TYPE}")
    print(f"  Top K Results: {TOP_K_RESULTS}")
    
    try:
        validate_config()
        print("\n✅ Configuration is valid!")
    except ValueError as e:
        print(f"\n❌ {e}")
