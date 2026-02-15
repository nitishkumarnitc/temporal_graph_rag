"""Search service for knowledge graph"""
from typing import List, Dict, Any, Optional
import re
from graphiti_core import Graphiti
from graphiti_core.llm_client import LLMClient
import json


class SearchService:
    """Service for searching the knowledge graph"""

    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti
        self.llm_client = graphiti.llm_client

    async def _enhance_query_with_llm(self, natural_query: str) -> str:
        """
        Use LLM to enhance natural language query by extracting key entities and concepts

        Converts: "What happened to David Chen?"
        Into: "David Chen departure left TechVision manager Engineering"

        Args:
            natural_query: Natural language question from user

        Returns:
            Enhanced query with entity names and key concepts
        """
        prompt = f"""You are a query enhancement assistant for a knowledge graph search system.

Your task: Convert a natural language question into a keyword-rich query that contains:
1. Entity names (people, companies, products, locations)
2. Key concepts and relationships
3. Action verbs and important context words

Rules:
- Extract all proper nouns (names, companies, products)
- Include relevant action words (left, joined, purchased, managed, etc.)
- Remove question words (what, when, where, who, how, why)
- Keep it concise (5-15 words)
- Return ONLY the enhanced query, no explanation

Examples:
Input: "What happened to David Chen?"
Output: David Chen departure left manager Engineering

Input: "What car did John Anderson buy?"
Output: John Anderson purchase buy car vehicle

Input: "Who reports to Sarah Martinez?"
Output: Sarah Martinez reports direct reports team members

Input: "Who has AWS certifications?"
Output: AWS certifications Solutions Architect Developer certified

Input: "When is my next service due?"
Output: service due maintenance schedule appointment next

Input: "What is John Anderson's complete customer journey?"
Output: John Anderson customer journey lead purchase delivery service

Now enhance this query:
Input: {natural_query}
Output:"""

        try:
            response = await self.llm_client.generate_response([{"role": "user", "content": prompt}])
            enhanced_query = response.strip()

            # Fallback to original if enhancement failed
            if not enhanced_query or len(enhanced_query) < 3:
                return natural_query

            return enhanced_query

        except Exception as e:
            # If LLM fails, return original query
            print(f"Warning: Query enhancement failed: {e}")
            return natural_query

    def _should_use_entity_filter(self, query: str) -> bool:
        """
        Auto-detect whether to use entity filter based on query characteristics

        Args:
            query: Search query text

        Returns:
            True if entity filter should be used, False for semantic search
        """
        # Check for proper nouns (capitalized words that aren't at start of sentence)
        words = query.split()
        capitalized_count = 0

        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word and len(clean_word) > 1:
                # Count capitalized words (excluding first word)
                if i > 0 and clean_word[0].isupper():
                    capitalized_count += 1

        # If query has 2+ capitalized words (likely entity names), use entity filter
        if capitalized_count >= 2:
            return True

        # Check for common question patterns that need semantic search
        question_patterns = [
            'what car', 'what vehicle', 'when is', 'where is', 'how much',
            'do you have', 'can i', 'tell me about'
        ]

        query_lower = query.lower()
        for pattern in question_patterns:
            if pattern in query_lower:
                return False

        # Default: use entity filter if query has at least one capitalized word
        return capitalized_count >= 1

    def _get_strategy_reason(self, query: str, use_entity_filter: bool) -> str:
        """
        Get human-readable explanation for why a strategy was chosen

        Args:
            query: Search query text
            use_entity_filter: Whether entity filter was chosen

        Returns:
            Explanation string
        """
        words = query.split()
        capitalized_count = sum(
            1 for i, word in enumerate(words)
            if i > 0 and re.sub(r'[^\w\s]', '', word) and re.sub(r'[^\w\s]', '', word)[0].isupper()
        )

        if use_entity_filter:
            if capitalized_count >= 2:
                return f"Found {capitalized_count} entity names (capitalized words) → use entity filter for precision"
            elif capitalized_count == 1:
                return "Found 1 entity name → use entity filter for precision"
            else:
                return "Manual override → entity filter"
        else:
            query_lower = query.lower()
            question_patterns = ['what car', 'what vehicle', 'when is', 'where is', 'how much', 'do you have', 'can i']
            for pattern in question_patterns:
                if pattern in query_lower:
                    return f"Generic question pattern '{pattern}' detected → use semantic search for recall"

            if capitalized_count == 0:
                return "No entity names found → use semantic search for recall"
            else:
                return "Manual override → semantic search"

    def _extract_entity_names(self, query: str) -> List[str]:
        """
        Extract potential entity names from query

        Heuristic: Look for words that might be entity names (proper nouns)
        - Capitalized words
        - Words that are likely names (not common words)

        Args:
            query: Search query text

        Returns:
            List of potential entity names
        """
        # Common question words, prepositions, and verbs to exclude
        stop_words = {
            'what', 'where', 'when', 'who', 'how', 'why', 'which',
            'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'at', 'to', 'for', 'of', 'on', 'with',
            'his', 'her', 'their', 'my', 'your', 'its',
            'working', 'work', 'works', 'role', 'job', 'position', 'title',
            'left', 'departure', 'purchase', 'buy', 'service', 'maintenance'
        }

        words = query.split()
        entity_names = []

        for word in words:
            # Clean punctuation
            clean_word = re.sub(r'[^\w\s]', '', word)
            if not clean_word:
                continue

            # Check if it's not a stop word (case-insensitive)
            if clean_word.lower() in stop_words:
                continue

            # Check if it starts with capital OR if it's a potential name
            # (we'll be lenient and include any non-stop-word that could be a name)
            if clean_word[0].isupper() or len(clean_word) > 2:
                # Capitalize first letter for consistency
                entity_names.append(clean_word.capitalize())

        return entity_names

    async def _find_entities_by_name(self, entity_names: List[str]) -> List[str]:
        """
        Find entity UUIDs by name (case-insensitive partial match)

        Args:
            entity_names: List of entity names to search for

        Returns:
            List of entity UUIDs
        """
        if not entity_names:
            return []

        # Build case-insensitive regex pattern for each name
        name_patterns = [f"(?i).*{re.escape(name)}.*" for name in entity_names]

        query = """
        MATCH (e:Entity)
        WHERE any(pattern IN $patterns WHERE e.name =~ pattern)
        RETURN e.uuid AS uuid, e.name AS name
        LIMIT 10
        """

        async with self.graphiti.driver.session() as session:
            result = await session.run(query, patterns=name_patterns)
            records = await result.data()
            return [record['uuid'] for record in records]

    async def _search_by_entities(
        self,
        entity_uuids: List[str],
        num_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for edges connected to specific entities

        Args:
            entity_uuids: List of entity UUIDs to search for
            num_results: Number of results to return

        Returns:
            List of edges connected to the entities
        """
        if not entity_uuids:
            return []

        # Query for edges where either source or target is one of the entities
        query = """
        MATCH (source:Entity)-[r:RELATES_TO]->(target:Entity)
        WHERE source.uuid IN $entity_uuids OR target.uuid IN $entity_uuids
        RETURN r.uuid AS uuid, r.fact AS fact, r.name AS name,
               r.created_at AS created_at, r.valid_at AS valid_at, r.expired_at AS expired_at
        ORDER BY r.created_at DESC
        LIMIT $limit
        """

        async with self.graphiti.driver.session() as session:
            result = await session.run(query, entity_uuids=entity_uuids, limit=num_results)
            records = await result.data()

            return [
                {
                    "fact": record['fact'],
                    "uuid": str(record['uuid']),
                    "name": record['name'],
                    "created_at": record['created_at'].isoformat() if record['created_at'] else None,
                    "valid_at": record['valid_at'].isoformat() if record['valid_at'] else None,
                    "expired_at": record['expired_at'].isoformat() if record['expired_at'] else None,
                }
                for record in records
            ]

    async def search(
        self,
        query: str,
        num_results: int = 5,
        group_ids: List[str] = None,
        min_score: float = 0.7,
        use_entity_filter: Optional[bool] = None,  # None = auto-detect
        enhance_query: bool = True  # Enable LLM-based query enhancement
    ) -> Dict[str, Any]:
        """
        Intelligent hybrid search with automatic strategy selection and LLM query enhancement

        Args:
            query: Search query (natural language)
            num_results: Number of results to return
            group_ids: Optional group IDs to filter by
            min_score: Minimum similarity score threshold (0.0-1.0)
            use_entity_filter: If None (default), auto-detect strategy. If True/False, override.
            enhance_query: If True, use LLM to enhance natural language query

        Returns:
            Dict with results and transformation metadata
        """
        # Store original query for logging
        original_query = query
        enhanced_query = query
        strategy_auto_detected = use_entity_filter is None

        # Step 1: Auto-detect strategy if not specified
        if use_entity_filter is None:
            use_entity_filter = self._should_use_entity_filter(query)
            strategy_reason = self._get_strategy_reason(query, use_entity_filter)
            print(f"🤖 Auto-detected strategy: {'Entity Filter' if use_entity_filter else 'Semantic Search'}")
            print(f"   Reason: {strategy_reason}")
        else:
            # Manual override
            strategy_reason = self._get_strategy_reason(query, use_entity_filter)

        # Step 2: Enhance query with LLM if enabled and using entity filter
        query_was_enhanced = False
        if enhance_query and use_entity_filter:
            enhanced_query = await self._enhance_query_with_llm(query)
            query_was_enhanced = enhanced_query != original_query
            if query_was_enhanced:
                print(f"🔍 Query Enhancement:")
                print(f"   Original: {original_query}")
                print(f"   Enhanced: {enhanced_query}")

        # Step 3: Try entity-based filtering if enabled
        search_method = "semantic_search"
        entity_names_found = []

        if use_entity_filter:
            entity_names = self._extract_entity_names(enhanced_query)
            entity_names_found = entity_names

            if entity_names:
                # Find entities in the graph
                entity_uuids = await self._find_entities_by_name(entity_names)

                if entity_uuids:
                    # Search for edges connected to these entities
                    entity_results = await self._search_by_entities(entity_uuids, num_results)

                    if entity_results:
                        # If we found results via entity filtering, return them
                        search_method = "entity_filter"
                        return {
                            "transformation": {
                                "original_query": original_query,
                                "enhanced_query": enhanced_query if query_was_enhanced else None,
                                "query_was_enhanced": query_was_enhanced,
                                "strategy_auto_detected": strategy_auto_detected,
                                "strategy_used": "entity_filter",
                                "strategy_reason": strategy_reason if strategy_auto_detected else "Manual override",
                                "entity_names_extracted": entity_names_found,
                                "search_method": search_method
                            },
                            "results": entity_results
                        }

        # Step 4: Fallback to semantic search if entity filtering didn't work or was disabled
        results = await self.graphiti.search(
            query=enhanced_query if enhance_query else query,
            num_results=num_results * 3,  # Get 3x results for better filtering
            group_ids=group_ids
        )

        # Filter and limit results
        filtered_results = results[:num_results]

        result_list = [
            {
                "fact": result.fact,
                "uuid": str(result.uuid),
                "name": result.name,
                "created_at": result.created_at.isoformat() if result.created_at else None,
                "valid_at": result.valid_at.isoformat() if result.valid_at else None,
                "expired_at": result.expired_at.isoformat() if result.expired_at else None,
            }
            for result in filtered_results
        ]

        return {
            "transformation": {
                "original_query": original_query,
                "enhanced_query": enhanced_query if query_was_enhanced else None,
                "query_was_enhanced": query_was_enhanced,
                "strategy_auto_detected": strategy_auto_detected,
                "strategy_used": "entity_filter" if use_entity_filter else "semantic_search",
                "strategy_reason": strategy_reason if strategy_auto_detected else "Manual override",
                "entity_names_extracted": entity_names_found,
                "search_method": search_method
            },
            "results": result_list
        }
    
    async def get_entity(self, entity_uuid: str) -> Dict[str, Any]:
        """
        Get entity by UUID with relationships
        
        Args:
            entity_uuid: Entity UUID
            
        Returns:
            Entity data with relationships
        """
        query = """
        MATCH (e:Entity {uuid: $uuid})
        OPTIONAL MATCH (e)-[r]->(related:Entity)
        RETURN e, collect({
            type: type(r),
            target: related.name,
            target_uuid: related.uuid
        }) as relationships
        """
        
        async with self.graphiti.driver.session() as session:
            result = await session.run(query, uuid=entity_uuid)
            record = await result.single()
            
            if not record:
                return None
            
            entity = record['e']
            relationships = record['relationships']
            
            return {
                "uuid": entity['uuid'],
                "name": entity.get('name'),
                "summary": entity.get('summary'),
                "created_at": entity.get('created_at'),
                "relationships": [r for r in relationships if r['target']]
            }
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get graph statistics
        
        Returns:
            Statistics about the knowledge graph
        """
        query = """
        MATCH (e:Entity)
        WITH count(e) as entity_count
        MATCH ()-[r:RELATES_TO]->()
        WITH entity_count, count(r) as rel_count
        MATCH (ep:Episodic)
        RETURN entity_count, rel_count, count(ep) as episode_count
        """
        
        async with self.graphiti.driver.session() as session:
            result = await session.run(query)
            record = await result.single()
            
            entities = record['entity_count']
            relationships = record['rel_count']
            episodes = record['episode_count']
            
            # Calculate graph density
            density = 0.0
            if entities > 1:
                max_edges = entities * (entities - 1)
                density = relationships / max_edges if max_edges > 0 else 0.0
            
            return {
                "entities": entities,
                "relationships": relationships,
                "episodes": episodes,
                "graph_density": round(density, 4),
                "avg_relationships_per_entity": round(relationships / entities, 2) if entities > 0 else 0
            }

