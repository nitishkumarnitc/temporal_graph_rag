"""Visualization service for knowledge graph"""
from typing import Dict, Any
from graphiti_core import Graphiti


class VisualizationService:
    """Service for visualizing the knowledge graph"""
    
    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti
    
    async def generate_mermaid_diagram(self, max_nodes: int = 20) -> str:
        """
        Generate Mermaid diagram of the knowledge graph
        
        Args:
            max_nodes: Maximum number of nodes to include
            
        Returns:
            Mermaid diagram as string
        """
        query = f"""
        MATCH (e1:Entity)-[r:RELATES_TO]->(e2:Entity)
        RETURN e1.name AS source, r.name AS relationship, e2.name AS target
        LIMIT {max_nodes}
        """
        
        async with self.graphiti.driver.session() as session:
            result = await session.run(query)
            relationships = await result.data()
        
        # Generate Mermaid diagram
        mermaid = "graph LR\n"
        
        for rel in relationships:
            source = rel['source'].replace('"', "'")
            target = rel['target'].replace('"', "'")
            rel_type = rel['relationship'].replace('"', "'")
            
            # Create node IDs (sanitize names)
            source_id = source.replace(" ", "_").replace("-", "_")
            target_id = target.replace(" ", "_").replace("-", "_")
            
            mermaid += f'    {source_id}["{source}"] -->|{rel_type}| {target_id}["{target}"]\n'
        
        return mermaid
    
    async def get_graph_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the graph for visualization
        
        Returns:
            Dict with graph summary data
        """
        query = """
        MATCH (e:Entity)
        WITH count(e) as entity_count
        MATCH ()-[r:RELATES_TO]->()
        WITH entity_count, count(r) as rel_count
        MATCH (ep:Episodic)
        WITH entity_count, rel_count, count(ep) as episode_count
        MATCH (e:Entity)-[r]-()
        RETURN entity_count, rel_count, episode_count,
               avg(size((e)-[]-()) ) as avg_degree
        """
        
        async with self.graphiti.driver.session() as session:
            result = await session.run(query)
            record = await result.single()
            
            return {
                "total_entities": record['entity_count'],
                "total_relationships": record['rel_count'],
                "total_episodes": record['episode_count'],
                "average_degree": round(record['avg_degree'], 2) if record['avg_degree'] else 0
            }

