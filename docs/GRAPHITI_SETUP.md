# Knowledge Graph RAG - Temporal Knowledge Graph with FastAPI

## 🎉 Schema-less Graph RAG with Runtime Entity Extraction

This project implements a **Temporal Knowledge Graph RAG** using Zep's Graphiti library with a schema-less FastAPI interface that extracts entities and relationships on-the-fly at runtime.

---

## 📦 What is Graphiti?

**Graphiti** is Zep's open-source temporal knowledge graph framework. It provides:

- **Three-tier Knowledge Graph Structure**:
  - **Episode Subgraph**: Raw input data (non-lossy storage)
  - **Semantic Entity Subgraph**: Extracted entities and relationships with entity resolution
  - **Community Subgraph**: High-level clusters of strongly connected entities

- **Bi-temporal Model**:
  - Timeline T: When events occurred (`valid_at`, `invalid_at`)
  - Timeline T': When we learned about them (`created_at`, `expired_at`)

- **Hybrid Retrieval**: Semantic embeddings + BM25 + graph traversal
- **Schema-less Design**: No predefined schemas - adapts to any data format

**GitHub**: https://github.com/getzep/graphiti
**Paper**: https://arxiv.org/html/2501.13956v1

---

## ✅ Current Implementation

### 1. **Technology Stack**
- ✅ `graphiti-core>=0.27.0` - Official Graphiti library
- ✅ **OpenAI LLM**: gpt-4o-mini (entity extraction and query processing)
- ✅ **OpenAI Embeddings**: text-embedding-3-small (1536 dimensions)
- ✅ **Neo4j 5.25**: Graph database with vector similarity
- ✅ **FastAPI**: REST API with async support
- ✅ **Docker + Colima**: Containerization for macOS

### 2. **FastAPI Application**
- ✅ **Schema-less Data Ingestion**: Accepts ANY data format (text, JSON, arrays)
- ✅ **Runtime Entity Extraction**: No predefined schemas required
- ✅ **CRUD Operations**: Full episode and entity management
- ✅ **Semantic Search**: Hybrid retrieval with temporal information
- ✅ **Error Handling**: Proper HTTP status codes for rate limits, auth, timeouts
- ✅ **OpenAPI Documentation**: Swagger UI and ReDoc

### 3. **Key Files**
- ✅ `src/api/routes.py` - FastAPI REST API
- ✅ `src/graphiti/client.py` - OpenAI client configuration
- ✅ `examples/general_data_ingestion.py` - General data ingestion examples
- ✅ `examples/general_queries.py` - Query examples
- ✅ `src/clean_database.py` - Database cleanup utility
- ✅ `docker-compose.yml` - API and Neo4j services

---

## 🚀 Quick Start

### Step 1: Set Up Environment Variables

```bash
cd graph_rag
cp .env.example .env
```

Edit `.env` and add:
```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=graph_rag
```

### Step 2: Start Services

```bash
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"
docker-compose up -d
```

This starts:
- **API**: http://localhost:8000
- **Neo4j Browser**: http://localhost:7474
- **Swagger UI**: http://localhost:8000/docs

### Step 3: Test the API

```bash
# Health check
curl http://localhost:8000/health

# Ingest data (schema-less!)
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"data": "Alice works at TechCorp as a software engineer"}'

# Search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Who works at TechCorp?"}'
```

---

## 📊 API Endpoints

### Core Operations
- `GET /` - API information
- `GET /health` - Health check with Graphiti connection status
- `GET /stats` - Graph statistics (entities, relationships, episodes)

### Data Ingestion (Schema-less!)
- `POST /ingest` - Universal data ingestion endpoint
  - Accepts: text, JSON objects, JSON arrays, nested structures
  - Extracts: entities, relationships, temporal information
  - No schema required!

### Search & Query
- `POST /search` - Semantic search with temporal context
  - Hybrid retrieval: embeddings + BM25 + graph traversal
  - Returns: entities, relationships, temporal information

### Episode Management
- `GET /episodes` - List all episodes (paginated)
- `DELETE /episodes/{uuid}` - Delete specific episode

### Entity Management
- `GET /entities` - List all entities (paginated)
- `GET /entities/{uuid}` - Get entity with relationships
- `DELETE /entities/{uuid}` - Delete specific entity

---

## 🔧 Configuration

### Environment Variables

```bash
# OpenAI Configuration (LLM and Embeddings)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=graph_rag
```

### OpenAI Rate Limits
- **Requests**: Depends on your tier (see OpenAI dashboard)
- **Tokens**: 6,000 per minute
- **Daily**: 100,000 tokens per day

---

## 📝 Example Usage

### Schema-less Data Ingestion

```python
import requests

# Ingest plain text
response = requests.post("http://localhost:8000/ingest", json={
    "data": "Alice Johnson joined TechCorp as VP of Engineering on 2024-01-15"
})

# Ingest JSON object
response = requests.post("http://localhost:8000/ingest", json={
    "data": {
        "employee": "Bob Smith",
        "role": "Senior Developer",
        "department": "Engineering",
        "skills": ["Python", "FastAPI", "Neo4j"]
    },
    "reference_time": "2024-02-01T00:00:00Z"
})

# Ingest with context
response = requests.post("http://localhost:8000/ingest", json={
    "data": "Project Alpha launched successfully",
    "context": "Q1 2024 milestone",
    "reference_time": "2024-03-15T00:00:00Z"
})
```

### Semantic Search

```python
# Search the knowledge graph
response = requests.post("http://localhost:8000/search", json={
    "query": "Who is the VP of Engineering?",
    "num_results": 5,
    "include_temporal": True
})

results = response.json()
for result in results["results"]:
    print(f"Entity: {result['name']}")
    print(f"Created: {result['created_at']}")
```

---

## 🧪 Three-Tier Graph Structure

When you ingest data, Graphiti automatically creates a three-tier knowledge graph:

### 1. Episode Subgraph (Raw Data)
- Stores original input data (non-lossy)
- Tracks when data was ingested (Timeline T')
- Links to extracted entities

### 2. Semantic Entity Subgraph (Extracted Knowledge)
- Entities: People, companies, projects, skills, etc.
- Relationships: works_at, reports_to, manages, has_skill, etc.
- Temporal tracking: when relationships became valid/invalid (Timeline T)
- Entity resolution: merges duplicate entities

### 3. Community Subgraph (High-level Clusters)
- Groups of strongly connected entities
- Useful for understanding organizational structure
- Enables community-based search

---

## 📚 Resources

- **Graphiti GitHub**: https://github.com/getzep/graphiti
- **Graphiti Docs**: https://help.getzep.com/graphiti
- **Zep Paper**: https://arxiv.org/html/2501.13956v1
- **Neo4j Browser**: http://localhost:7474
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🐳 Docker Commands

```bash
# Start all services
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"
docker-compose up -d

# View API logs
docker-compose logs -f api

# Restart API
docker-compose restart api

# Stop all services
docker-compose down

# Clean database
python src/clean_database.py
```

---

## ✨ Key Features

- ✅ **Schema-less Design** - No predefined schemas, adapts to any data
- ✅ **Runtime Extraction** - Entities/relationships extracted on-the-fly
- ✅ **Bi-temporal Model** - Track event time vs ingestion time
- ✅ **Hybrid Retrieval** - Semantic + BM25 + graph traversal
- ✅ **Entity Resolution** - Automatic merging of duplicate entities
- ✅ **Production Ready** - Error handling, rate limiting, monitoring
- ✅ **OpenAI Powered** - gpt-4o-mini for LLM, text-embedding-3-small for embeddings

---

**Status**: ✅ Production Ready
**API**: http://localhost:8000
**Docs**: http://localhost:8000/docs
**Graphiti Version**: 0.27.1

