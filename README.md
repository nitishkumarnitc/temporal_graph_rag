# Temporal Graph RAG: Time-Aware Knowledge Graphs for AI Memory

> **Why Intelligence is Not Just About Retrieving Facts — It's About Understanding How Facts Change**

## Overview

**Temporal Graph RAG** is a framework that extends traditional Retrieval-Augmented Generation (RAG) with time-aware knowledge modeling. While basic RAG treats knowledge as static, Temporal Graph RAG introduces temporal dimensions to track how facts evolve, relationships change, and events unfold over time.

### The Problem with Traditional RAG

Conventional RAG systems have a critical blind spot:
- **No native concept of time** — Old and new information coexist without explicit validity
- **Fragmented knowledge representation** — Retrieval operates on text snippets, not structured facts
- **Weak reasoning over relationships** — Connections between entities are implicit rather than modeled

In real-world systems, this leads to **temporally inconsistent** responses. For example, asking "Who manages the platform team?" when leadership has recently changed may return a confident but incorrect answer grounded in outdated documents.

### Why Time-Aware Retrieval Matters

Temporal Graph RAG models knowledge as **dynamic** rather than static:
- Facts carry timestamps or validity ranges
- Relationship changes are preserved as history
- Queries are evaluated relative to time
- Instead of overwriting knowledge, the system tracks evolution

This enables:
- ✅ Historical reasoning
- ✅ Change detection and conflict resolution
- ✅ Temporal filtering and validity checking
- ✅ More accurate context retrieval for LLM applications
- ✅ Better support for evolving organizational knowledge

## Key Use Cases

Temporal Graph RAG becomes essential in:
- **AI Agent Memory Systems** — Maintaining accurate context over time
- **Organizational Knowledge** — Tracking role changes, team restructures, and policy updates
- **User Preference Evolution** — Understanding how user preferences and behavior change
- **Financial & Compliance Data** — Maintaining audit trails and historical accuracy
- **Event-Driven Architectures** — Modeling systems where state changes matter
- **Audit & History Tracking** — Preserving what was true, when it became true, and what changed

## Architecture

### Core Components

- **LLMs**: OpenAI (gpt-4o-mini) — Entity/fact extraction and query processing
- **Embeddings**: OpenAI text-embedding-3-small — High-quality, cost-effective embeddings
- **Graph Database**: Neo4j 5.25+ — Knowledge graph storage with temporal information
- **Graph RAG Library**: Zep Graphiti — Temporal knowledge graph framework
- **Containerization**: Docker + Colima (macOS)

### How It Works

1. **Ingests Data**: Accepts temporal events with tenant and customer context
2. **Creates Episodes**: Converts data into temporal episodes
3. **Extracts Entities**: Uses OpenAI to identify people, organizations, etc.
4. **Extracts Facts**: Identifies relationships between entities with temporal validity
5. **Builds Knowledge Graph**: Stores in Neo4j with temporal information
6. **Enables Search**: Supports natural language queries with multi-tenant isolation and temporal filtering

## Project Structure

```
temporal_graph_rag/
├── src/
│   ├── api/                    # FastAPI application
│   ├── graphiti/               # Graphiti integration
│   └── scripts/                # Utility scripts
├── examples/                    # Example scripts and data
├── docs/                        # Documentation
├── tests/                       # Test files
├── docker-compose.yml          # Neo4j + Colima setup
├── Dockerfile                  # Application container
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

1. **OpenAI API Key** — Get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. **Docker Desktop** — For running Neo4j
3. **Python 3.11+** — For running the application

### 1. Configure Environment

```bash
cp .env.example .env
# Edit .env with your OpenAI API key and configuration
```

### 2. Start Services

```bash
# Start Neo4j and Colima
docker-compose up -d neo4j

# Wait for Neo4j to be ready (30-40 seconds)
sleep 40
```

### 3. Run the Application

```bash
# Start the FastAPI server
python -m uvicorn src.api.routes:app --host 0.0.0.0 --port 8000
```

## 📊 What It Does

1. **Ingest Data** — Accepts temporal events with tenant and customer context
2. **Create Episodes** — Converts data into temporal episodes
3. **Extract Entities** — Uses OpenAI to extract entities (people, organizations, etc.)
4. **Extract Facts** — Identifies relationships between entities
5. **Build Knowledge Graph** — Stores in Neo4j with temporal information
6. **Enable Search** — Natural language queries with multi-tenant isolation

## 🔧 Configuration

### OpenAI Setup

1. Get your API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Models used:
   - `gpt-4o-mini` — LLM for entity extraction and query processing
   - `text-embedding-3-small` — Embeddings (high quality, cost-effective)

**Configuration Options**:
- **No API key needed** — Runs locally in Docker
- **First run** — Downloads model (~90MB) automatically

### Neo4j Access

- **Web UI**: [http://localhost:7474](http://localhost:7474)
- **Bolt**: bolt://localhost:7687
- **Username**: neo4j
- **Password**: graph_rag

## 📝 Sample Data

The system includes sample data for TechCorp Solutions:
- Employee organizational structure
- Department relationships
- Project assignments with temporal changes
- Skill mappings

## 🛠️ Development

### Run Examples

```bash
python examples/basic_example.py
```

### Run Tests

```bash
pytest tests/
```

### Clean Up

```bash
# Stop and remove containers
docker-compose down -v

# Remove volumes to reset database
docker volume prune
```

## 📚 Documentation

For detailed documentation, see:
- `docs/architecture.md` — System design and components
- `docs/api.md` — API reference
- `docs/examples.md` — Usage examples
- `docs/deployment.md` — Production deployment guide

## 🔍 Troubleshooting

### OpenAI API Key Error

Error: `"Fail to get model gpt-4o-mini"`

**Solution**: Ensure your API key is set in `.env`:
```bash
OPENAI_API_KEY=sk-...
```
Get your key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Neo4j Connection Refused

Error: `"Connection refused" at localhost:7687`

**Solution**: Ensure Neo4j is running:
```bash
docker-compose up -d neo4j
sleep 40  # Wait for startup
```

### Embedding Model Download

If the embedding model fails to download, try:
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

## 📄 License

MIT License - See LICENSE file for details

## 🔗 References

Based on concepts from:
- [Temporal Graph RAG: Why Time-Aware Knowledge Graphs Are Reshaping AI Memory](https://medium.com/@nitishkumarnitc/temporal-graph-rag-why-time-aware-knowledge-graphs-are-reshaping-ai-memory-04fc62dd0acd)
- [Zep Graphiti - Temporal Knowledge Graph Framework](https://github.com/getzep/graphiti)
