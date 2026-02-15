# Knowledge Graph RAG - Dependencies Setup

## Overview

This project uses:

- **OpenAI** for LLM + embeddings
- **Zep Graphiti (`graphiti-core`)** for temporal knowledge graphs
- **Neo4j** as the graph database
- **FastAPI + Uvicorn** for the API

The actual Python dependencies are defined in `requirements.txt` and are kept
minimal to match the codebase.

## Python Dependencies

Current `requirements.txt` (simplified):

- `graphiti-core>=0.27.0` – Temporal knowledge graph & RAG framework
- `python-dotenv>=1.0.0` – Environment variable management
- `pandas>=2.1.0` – Data manipulation utilities (used in examples/utilities)
- `faker>=22.0.0` – Synthetic data generation for examples
- `matplotlib>=3.8.0` – Optional visualization
- `plotly>=5.18.0` – Optional interactive plots
- `pytest>=7.4.0` – Testing
- `pytest-asyncio>=0.23.0` – Async testing
- `fastapi>=0.109.0` – API framework
- `uvicorn[standard]>=0.27.0` – ASGI server

> Note: `graphiti-core` brings in its own required dependencies (including
> Neo4j/driver support) via PyPI.

## Installing Dependencies Locally

From the `graph_rag` directory:

```bash
pip install -r requirements.txt
```

Make sure you are using Python 3.11+ and a virtual environment (recommended).

### Environment

Create `.env`:

```bash
cp .env.example .env
```

Then set at least:

```bash
OPENAI_API_KEY=your_openai_api_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=graph_rag
```

## Running the API Locally (Without Docker)

1. Start Neo4j (locally or via Docker):

```bash
docker run -d \
  --name neo4j-graphrag \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/graph_rag \
  -e NEO4J_PLUGINS='["apoc","graph-data-science"]' \
  neo4j:5.25
```

2. Start the FastAPI app:

```bash
cd graph_rag
uvicorn src.api.routes:app --host 0.0.0.0 --port 8000
```

3. Check health:

```bash
curl http://localhost:8000/health
```

## Running Tests

With API running on `http://localhost:8000`:

```bash
cd graph_rag/tests
pytest test_graph_quality.py -v -s
```

Tests will:

- Ingest data via the `/ingest` endpoint
- Validate bi-temporal modeling
- Check entity and relationship extraction
- Verify graph statistics

## Notes

- No Gemini / Groq dependencies are required – the project is **OpenAI-only**.
- If you add extra libraries (for your own experiments), keep them in sync with
  `requirements.txt`.

