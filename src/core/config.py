"""Configuration management for Temporal Knowledge Graph RAG System"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Centralized configuration management"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
    CACHE_DIR = Path(os.getenv("CACHE_DIR", BASE_DIR / "cache"))

    # OpenAI Configuration (LLM + Embeddings)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini")
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    OPENAI_EMBEDDING_DIM = int(os.getenv("OPENAI_EMBEDDING_DIM", "1536"))
    
    # Neo4j Configuration
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "graph_rag")
    
    # Application Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    API_VERSION = "1.0.0"

    # Rate Limiting Configuration
    ENABLE_RATE_LIMIT_DELAY = os.getenv("ENABLE_RATE_LIMIT_DELAY", "false").lower() == "true"
    RATE_LIMIT_DELAY_MS = int(os.getenv("RATE_LIMIT_DELAY_MS", "2000"))
    RATE_LIMIT_ITERATION_DELAY_MS = int(os.getenv("RATE_LIMIT_ITERATION_DELAY_MS", "3000"))

    # Display settings
    BANNER_WIDTH = 80
    SEPARATOR_CHAR = "="
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories"""
        for directory in [cls.DATA_DIR, cls.CACHE_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Validate required configuration (OpenAI-only)"""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY must be set.\n"
                "Get your API key from: https://platform.openai.com/api-keys"
            )
    
    @classmethod
    def get_summary(cls) -> dict:
        """Get configuration summary"""
        summary = {
            "llm_provider": "openai",
            "embedding_model": cls.OPENAI_EMBEDDING_MODEL,
            "embedding_dim": cls.OPENAI_EMBEDDING_DIM,
            "neo4j_uri": cls.NEO4J_URI,
            "data_dir": str(cls.DATA_DIR),
            "log_level": cls.LOG_LEVEL,
            "api_version": cls.API_VERSION,
            "rate_limit_enabled": cls.ENABLE_RATE_LIMIT_DELAY,
        }

        # Model info (OpenAI-only)
        summary["llm_model"] = f"{cls.OPENAI_LLM_MODEL} (OpenAI)"

        if cls.ENABLE_RATE_LIMIT_DELAY:
            summary["rate_limit_delay"] = f"{cls.RATE_LIMIT_DELAY_MS}ms"
            summary["iteration_delay"] = f"{cls.RATE_LIMIT_ITERATION_DELAY_MS}ms"

        return summary
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        config = cls.get_summary()
        print(f"\n{cls.SEPARATOR_CHAR * cls.BANNER_WIDTH}")
        print("TEMPORAL KNOWLEDGE GRAPH RAG CONFIGURATION")
        print(f"{cls.SEPARATOR_CHAR * cls.BANNER_WIDTH}")
        for key, value in config.items():
            print(f"  {key}: {value}")
        print(f"{cls.SEPARATOR_CHAR * cls.BANNER_WIDTH}\n")


# Ensure directories exist on import
Config.ensure_directories()

