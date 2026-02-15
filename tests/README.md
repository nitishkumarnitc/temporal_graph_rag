# Graph RAG Test Suite

## Overview

This test suite validates the three-tier knowledge graph structure and quality of entity/relationship extraction.

## Test Files

### `test_graph_quality.py`
Comprehensive test suite that validates:

1. **Episode Subgraph** - Raw data storage (non-lossy)
2. **Semantic Entity Subgraph** - Entity and relationship extraction
3. **Community Subgraph** - High-level clustering (managed by Graphiti)
4. **Bi-temporal Model** - Timeline T (event time) vs Timeline T' (ingestion time)
5. **Hybrid Retrieval** - Semantic + BM25 + graph traversal
6. **Entity Resolution** - Duplicate detection and merging

## Running Tests

### Prerequisites

You need:

- A running Neo4j instance (local or Docker)
- The FastAPI app running on `http://localhost:8000`

#### Option 1: Run everything locally

1. Start Neo4j (Docker example):

```bash
docker run -d \
  --name neo4j-graphrag \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/graph_rag \
  -e NEO4J_PLUGINS='["apoc","graph-data-science"]' \
  neo4j:5.25
```

2. Start the API from the project root:

```bash
cd graph_rag
uvicorn src.api.routes:app --host 0.0.0.0 --port 8000
```

3. In another terminal, verify health:

```bash
curl http://localhost:8000/health
```

#### Option 2: Use docker-compose

From `graph_rag/`:

```bash
docker compose up -d
curl http://localhost:8000/health
```

### Run All Tests
```bash
# Install pytest if needed
pip install pytest pytest-asyncio

# Run with verbose output
cd graph_rag/tests
pytest test_graph_quality.py -v -s

# Run specific test
pytest test_graph_quality.py::TestGraphQuality::test_01_health_check -v -s
```

## Test Scenarios

### Test 1: Health Check
Verifies API is running and Graphiti is connected.

### Test 2: Episode Subgraph - Text Ingestion
- Ingests plain text data
- Verifies episode creation
- Checks Timeline T (reference_time) and Timeline T' (ingested_at)

### Test 3: Episode Subgraph - JSON Ingestion
- Ingests structured JSON data
- Verifies schema-less ingestion works for complex objects

### Test 4: Semantic Entity Extraction
- Ingests data with clear entities (person, organization, skills)
- Verifies entities are extracted automatically
- Lists sample entities

### Test 5: Semantic Relationships
- Checks relationship extraction quality
- Calculates relationship/entity ratio
- Validates graph connectivity

### Test 6: Bi-Temporal Tracking
- Ingests historical data with past reference_time
- Verifies Timeline T ≠ Timeline T'
- Validates temporal tracking

### Test 7: Hybrid Search
- Performs semantic search
- Tests hybrid retrieval (embeddings + BM25 + graph)
- Displays top results with temporal info

### Test 8: Entity Resolution
- Ingests same entity mentioned in different ways
- Tests duplicate detection
- Checks if entities are merged

### Test 9: Graph Statistics Summary
- Final comprehensive statistics
- Validates three-tier structure
- Calculates graph density
- Quality checks

## Expected Output

```
================================================================================
TEST: Episode Subgraph - Text Ingestion
================================================================================
✅ Episode created: Data ingestion at 2024-02-12 10:30:45
   Reference time (T): 2024-01-15T09:00:00+00:00
   Ingested at (T'): 2024-02-12T10:30:45.123456
✅ Total episodes in graph: 5

================================================================================
TEST: Semantic Entity Subgraph - Entity Extraction
================================================================================
📊 Current graph state:
   Entities: 15
   Relationships: 23
   Episodes: 5

✅ Entities extracted: 18

📋 Sample entities:
   - Sarah Chen (created: 2024-02-12T10:30:48.123456)
   - DataCorp (created: 2024-02-12T10:30:48.234567)
   - Chief Data Officer (created: 2024-02-12T10:30:48.345678)

================================================================================
TEST: Final Graph Statistics Summary
================================================================================

📊 FINAL GRAPH STATE:
   ============================================================
   Episodes (Raw Data):        8
   Entities (Extracted):       25
   Relationships (Extracted):  42
   ============================================================
   Graph Density:              0.0700

✅ THREE-TIER GRAPH STRUCTURE VERIFIED:
   1. Episode Subgraph:        8 episodes
   2. Semantic Entity Subgraph: 25 entities, 42 relationships
   3. Community Subgraph:       (managed by Graphiti)

✅ Graph quality checks passed!
```

## Rate Limit Handling

Tests gracefully handle OpenAI rate limits:
- If rate limit is hit (HTTP 429), test is skipped with warning
- Tests continue with remaining scenarios
- No test failures due to rate limits

## Notes

- Tests are designed to be idempotent (can run multiple times)
- Each test waits 2-3 seconds for graph processing
- Tests use realistic organizational data scenarios
- Entity resolution depends on LLM capability

