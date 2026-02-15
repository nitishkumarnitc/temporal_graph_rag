"""Client initialization for LLM, embeddings, and cross-encoder (OpenAI-only)"""
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.cross_encoder.openai_reranker_client import OpenAIRerankerClient

from .config import Config


def get_llm_client():
    """Get OpenAI LLM client"""
    Config.validate()

    llm_config = LLMConfig(
        api_key=Config.OPENAI_API_KEY,
        model=Config.OPENAI_LLM_MODEL,
        small_model=Config.OPENAI_LLM_MODEL,
    )
    return OpenAIClient(config=llm_config)


def get_embedder():
    """
    Get OpenAI embedder client
    
    Returns:
        OpenAIEmbedder: Configured OpenAI embedder
    """
    Config.validate()
    
    return OpenAIEmbedder(
        config=OpenAIEmbedderConfig(
            api_key=Config.OPENAI_API_KEY,
            embedding_model=Config.OPENAI_EMBEDDING_MODEL,
            embedding_dim=Config.OPENAI_EMBEDDING_DIM,
        )
    )


def get_cross_encoder():
    """Get OpenAI-based reranker client"""
    Config.validate()

    # Get LLM client and config for reranking (OpenAI-only)
    llm_client = get_llm_client()
    llm_config = LLMConfig(
        api_key=Config.OPENAI_API_KEY,
        model=Config.OPENAI_LLM_MODEL,
        small_model=Config.OPENAI_LLM_MODEL,
    )

    return OpenAIRerankerClient(client=llm_client, config=llm_config)


def get_all_clients():
    """Get all clients (LLM, embedder, cross-encoder)"""
    print("🤖 Configuring OpenAI clients")
    print(f"  - LLM Model: {Config.OPENAI_LLM_MODEL} (OpenAI)")
    print(f"  - Embedding Model: {Config.OPENAI_EMBEDDING_MODEL} (OpenAI)")

    if Config.ENABLE_RATE_LIMIT_DELAY:
        print(f"  - Rate Limiting: Enabled ({Config.RATE_LIMIT_DELAY_MS}ms delay)")
    else:
        print(f"  - Rate Limiting: Disabled")
    print()

    return (
        get_llm_client(),
        get_embedder(),
        get_cross_encoder()
    )

