"""Export service for knowledge graph"""
import json
from typing import Dict, Any, List
from pathlib import Path
from graphiti_core import Graphiti
from src.core.config import Config


class ExportService:
    """Service for exporting knowledge graph data"""
    
    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti
    
    async def export_to_json(self, output_file: Path = None) -> Dict[str, Any]:
        """
        Export entire graph to JSON
        
        Args:
            output_file: Optional output file path
            
        Returns:
            Dict with entities, relationships, and episodes
        """
        # Get all entities
        entities_query = """
        MATCH (e:Entity)
        RETURN e.uuid AS uuid, e.name AS name, e.summary AS summary,
               e.created_at AS created_at, e.valid_at AS valid_at
        ORDER BY e.created_at DESC
        """
        
        # Get all relationships
        relationships_query = """
        MATCH (e1:Entity)-[r:RELATES_TO]->(e2:Entity)
        RETURN e1.uuid AS source_uuid, e1.name AS source_name,
               e2.uuid AS target_uuid, e2.name AS target_name,
               r.name AS relationship_type,
               r.created_at AS created_at
        ORDER BY r.created_at DESC
        """
        
        # Get all episodes
        episodes_query = """
        MATCH (ep:Episodic)
        RETURN ep.uuid AS uuid, ep.name AS name, ep.content AS content,
               ep.created_at AS created_at, ep.valid_at AS valid_at,
               ep.source AS source
        ORDER BY ep.created_at DESC
        """
        
        async with self.graphiti.driver.session() as session:
            # Fetch entities
            result = await session.run(entities_query)
            entities = await result.data()
            
            # Fetch relationships
            result = await session.run(relationships_query)
            relationships = await result.data()
            
            # Fetch episodes
            result = await session.run(episodes_query)
            episodes = await result.data()
        
        export_data = {
            "metadata": {
                "exported_at": json.dumps(None),  # Will be set below
                "total_entities": len(entities),
                "total_relationships": len(relationships),
                "total_episodes": len(episodes)
            },
            "entities": entities,
            "relationships": relationships,
            "episodes": episodes
        }
        
        # Save to file if specified
        if output_file:
            output_file = Path(output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            print(f"✅ Exported to {output_file}")
        
        return export_data
    
    async def export_cypher_queries(self, output_file: Path = None) -> str:
        """
        Export useful Cypher queries
        
        Args:
            output_file: Optional output file path
            
        Returns:
            String with Cypher queries
        """
        queries = """
-- Temporal Knowledge Graph - Useful Cypher Queries

-- Get all entities
MATCH (e:Entity)
RETURN e.name AS entity, e.summary AS summary, e.created_at AS created
ORDER BY e.created_at DESC
LIMIT 20;

-- Get all relationships
MATCH (e1:Entity)-[r:RELATES_TO]->(e2:Entity)
RETURN e1.name AS source, r.name AS relationship, e2.name AS target
ORDER BY r.created_at DESC
LIMIT 20;

-- Get all episodes
MATCH (ep:Episodic)
RETURN ep.name AS episode, ep.created_at AS created, ep.content AS content
ORDER BY ep.created_at DESC
LIMIT 20;

-- Find entities with most relationships
MATCH (e:Entity)-[r]-()
RETURN e.name AS entity, count(r) AS relationship_count
ORDER BY relationship_count DESC
LIMIT 10;

-- Get graph statistics
MATCH (e:Entity)
WITH count(e) as entities
MATCH ()-[r:RELATES_TO]->()
WITH entities, count(r) as relationships
MATCH (ep:Episodic)
RETURN entities, relationships, count(ep) as episodes;
"""
        
        if output_file:
            output_file = Path(output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w') as f:
                f.write(queries)
            
            print(f"✅ Exported Cypher queries to {output_file}")
        
        return queries

