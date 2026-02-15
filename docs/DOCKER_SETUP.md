# Knowledge Graph RAG - Docker Setup (Neo4j + API)

This guide shows how to run Neo4j and the FastAPI service using Docker.

## 🐳 Prerequisites

- Docker Desktop (macOS, Windows) or Docker Engine (Linux)
- An OpenAI API key: https://platform.openai.com/api-keys

## 📁 Project Layout (Docker-relevant)

- `docker-compose.yml` – defines:
  - `neo4j` (graph database)
  - `api` (FastAPI app exposing `/ingest`, `/search`, etc.)
- `.env.example` – environment variable template

## ⚙️ Configure Environment

1. Create your `.env` file from the template:

```bash
cd graph_rag
cp .env.example .env
```

2. Edit `.env` and set at least:

```bash
OPENAI_API_KEY=your_openai_api_key_here
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=graph_rag
```

## 🚀 Start Neo4j + API via Docker Compose

From the `graph_rag` directory:

```bash
docker compose up -d
```

This will:
- Start Neo4j (container name: `neo4j-graphrag`)
- Start the FastAPI app (container name: `graph-rag-api`)

### Verify Services

```bash
# Check containers
docker compose ps

# Check API health
curl http://localhost:8000/health
```

Neo4j Web UI:

- http://localhost:7474  
- Username: `neo4j`  
- Password: `graph_rag`

## 🔄 Using the Examples

Once the API & Neo4j are running:

```bash
# From graph_rag/
bash examples/run_general_ingestion.sh
bash examples/run_general_queries.sh
```

These scripts will talk to `http://localhost:8000`.

## 🧹 Clearing Neo4j Data

To wipe all nodes and relationships from the running Neo4j container:

```bash
bash examples/clear_neo4j.sh
```

This uses the `neo4j-graphrag` container created by `docker-compose.yml`.

## 🛑 Stopping and Cleaning Up

```bash
# Stop containers
docker compose down

# Stop and remove containers + volumes (deletes Neo4j data)
docker compose down -v
```

## ❓ Troubleshooting

### API not reachable

- Check containers:

```bash
docker compose ps
docker compose logs api
```

### Neo4j connection errors

- Make sure Neo4j is healthy:

```bash
docker compose logs neo4j
```

- Confirm `NEO4J_URI`, `NEO4J_USER`, and `NEO4J_PASSWORD` in `.env` match `docker-compose.yml`.

### OpenAI authentication errors

- Verify `OPENAI_API_KEY` is set in `.env` and that the container sees it:

```bash
docker compose exec api env | grep OPENAI_API_KEY
```

If missing, stop the stack, fix `.env`, and run `docker compose up -d` again.

