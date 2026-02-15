"""Database connection and management"""
from graphiti_core import Graphiti
from .config import Config
from .clients import get_all_clients


_graphiti_instance = None


def get_graphiti_instance(force_new=False):
    """
    Get or create Graphiti instance (singleton pattern)
    
    Args:
        force_new: Force creation of new instance
        
    Returns:
        Graphiti: Configured Graphiti instance
    """
    global _graphiti_instance
    
    if _graphiti_instance is None or force_new:
        llm_client, embedder, cross_encoder = get_all_clients()

        _graphiti_instance = Graphiti(
            uri=Config.NEO4J_URI,
            user=Config.NEO4J_USER,
            password=Config.NEO4J_PASSWORD,
            llm_client=llm_client,
            embedder=embedder,
            cross_encoder=cross_encoder
        )
    
    return _graphiti_instance


async def close_graphiti_instance():
    """Close the Graphiti instance"""
    global _graphiti_instance
    
    if _graphiti_instance:
        await _graphiti_instance.close()
        _graphiti_instance = None


async def build_indices():
    """Build Neo4j indices and constraints"""
    graphiti = get_graphiti_instance()
    print("🔧 Building indices and constraints...")
    await graphiti.build_indices_and_constraints()
    print("✅ Indices built")

