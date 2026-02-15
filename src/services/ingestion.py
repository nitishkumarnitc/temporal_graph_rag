"""Data ingestion service"""
from datetime import datetime
from typing import Dict, Any, Union, List
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType


class DataIngestionService:
    """Service for ingesting data into the knowledge graph"""
    
    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti
    
    async def ingest_text(
        self,
        text: str,
        reference_time: datetime = None,
        context: str = None,
        group_ids: List[str] = None
    ) -> Dict[str, Any]:
        """
        Ingest plain text data

        Args:
            text: Text content to ingest
            reference_time: When the event occurred (Timeline T)
            context: Additional context for entity extraction
            group_ids: Optional group IDs for tenant isolation

        Returns:
            Dict with episode UUID and metadata
        """
        if reference_time is None:
            reference_time = datetime.now()

        # Add context to help with extraction
        episode_body = f"{context}\n\n{text}" if context else text

        # Use a human-readable episode name and reuse it in the response
        episode_name = f"Text ingestion at {datetime.now().isoformat()}"

        result = await self.graphiti.add_episode(
            name=episode_name,
            episode_body=episode_body,
            source=EpisodeType.text,
            source_description=context or "Text data ingestion",
            reference_time=reference_time,
            group_id=group_ids[0] if group_ids else None
        )

        return {
            "status": "success",
            "episode_uuid": str(result.episode.uuid),
            "episode_name": episode_name,
            "ingested_at": datetime.now().isoformat(),
            "reference_time": reference_time.isoformat(),
            "group_id": group_ids[0] if group_ids else None,
            "type": "text",
            "data_type": "str",
        }

    async def ingest_json(
        self,
        data: Union[Dict, List],
        reference_time: datetime = None,
        context: str = None,
        group_ids: List[str] = None
    ) -> Dict[str, Any]:
        """
        Ingest JSON data (schema-less)

        Args:
            data: JSON data (dict or list)
            reference_time: When the event occurred (Timeline T)
            context: Additional context for entity extraction
            group_ids: Optional group IDs for tenant isolation

        Returns:
            Dict with episode UUID and metadata
        """
        import json

        if reference_time is None:
            reference_time = datetime.now()

        # Convert JSON to text for LLM processing
        json_text = json.dumps(data, indent=2)
        episode_body = f"{context}\n\n{json_text}" if context else json_text

        # Keep a readable episode name and expose it in the response
        episode_name = f"JSON ingestion at {datetime.now().isoformat()}"

        result = await self.graphiti.add_episode(
            name=episode_name,
            episode_body=episode_body,
            source=EpisodeType.json,
            source_description=context or "JSON data ingestion",
            reference_time=reference_time,
            group_id=group_ids[0] if group_ids else None
        )

        # Determine original JSON data type (dict vs list)
        data_type = type(data).__name__

        return {
            "status": "success",
            "episode_uuid": str(result.episode.uuid),
            "episode_name": episode_name,
            "ingested_at": datetime.now().isoformat(),
            "reference_time": reference_time.isoformat(),
            "group_id": group_ids[0] if group_ids else None,
            "type": "json",
            "data_type": data_type,
        }
    
    async def ingest_data(
        self,
        data: Union[str, Dict, List],
        reference_time: datetime = None,
        context: str = None,
        group_ids: List[str] = None
    ) -> Dict[str, Any]:
        """
        Universal data ingestion - automatically detects type

        Args:
            data: Data in any format (text, dict, list)
            reference_time: When the event occurred (Timeline T)
            context: Additional context for entity extraction
            group_ids: Optional group IDs for tenant isolation

        Returns:
            Dict with episode UUID and metadata
        """
        if isinstance(data, str):
            return await self.ingest_text(data, reference_time, context, group_ids)
        else:
            return await self.ingest_json(data, reference_time, context, group_ids)

