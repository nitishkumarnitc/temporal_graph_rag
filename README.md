# Knowledge Graph RAG - OpenAI + Zep Graphiti

A Graph RAG (Retrieval-Augmented Generation) system using OpenAI (LLM and embeddings) and Zep's Graphiti library for temporal knowledge graphs.

## 🏗️ Architecture

- **LLM**: OpenAI (gpt-4o-mini) - Entity/fact extraction and query processing
- **Embeddings**: OpenAI (text-embedding-3-small) - High quality, cost-effective
- **Graph Database**: Neo4j 5.25 - Knowledge graph storage
- **Graph RAG Library**: Zep Graphiti - Temporal knowledge graph framework
- **Containerization**: Docker + Colima (macOS)

## 📁 Project Structure

```
graph_rag/
├── src/
│   ├── api/                 # FastAPI application
│   ├── graphiti/            # Graphiti integration
│   └── scripts/             # Utility scripts
├── examples/                # Example scripts and data
├── docs/                    # Documentation
├── tests/                   # Test files
├── docker-compose.yml       # Docker services configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop or Colima (for macOS)
- OpenAI API key: https://platform.openai.com/api-keys

### 1. Configure Environment

Edit the `.env` file and add your API keys:

```bash
# OpenAI Configuration (for LLM and Embeddings)
OPENAI_API_KEY=your_openai_api_key_here

# Neo4j Configuration
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=graph_rag

# Application Settings
LOG_LEVEL=INFO
DATA_DIR=./data
```

### 2. Start Services

```bash
# For Colima (macOS)
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"

# Start Neo4j
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

1. **Ingests Data**: Accepts temporal events with tenant and customer context
2. **Creates Episodes**: Converts data into temporal episodes
3. **Extracts Entities**: Uses OpenAI to extract entities (people, organizations, etc.)
4. **Extracts Facts**: Identifies relationships between entities
5. **Builds Knowledge Graph**: Stores in Neo4j with temporal information
6. **Enables Search**: Natural language queries with multi-tenant isolation

## 🔧 Configuration

### OpenAI Setup

1. **Get API Key**: https://platform.openai.com/api-keys
2. **Models Used**:
   - `gpt-4o-mini` (LLM for entity extraction and query processing)
   - `text-embedding-3-small` (Embeddings)
- **No API key needed** - runs locally in Docker
- **First run**: Downloads model (~90MB) automatically

### Neo4j Access

- **Web UI**: http://localhost:7474
- **Bolt**: bolt://localhost:7687
- **Username**: neo4j
- **Password**: graph_rag

## 📝 Sample Data

The system includes sample data for TechCorp Solutions:
- 10 employees across different levels (L4-L8, Executive)
- 2 departments (Engineering, Product)
- 3 projects
- Skills, roles, and relationships

## 🛠️ Development

### Run Examples

```bash
# Run example ingestion
bash examples/run_general_ingestion.sh

# Run example queries
bash examples/run_general_queries.sh
```

### Clean Up

```bash
# Stop all services
docker-compose down

# Remove volumes (deletes Neo4j data)
docker-compose down -v
```

## 📚 Documentation

See the `docs/` folder for detailed documentation:
- `DOCKER_SETUP.md` - Docker and Colima setup
- `GRAPHITI_SETUP.md` - Graphiti library details
- `DEPENDENCIES_SETUP.md` - Python dependencies
- `QUICKSTART.md` - Quick start guide

## 🔍 Troubleshooting

### OpenAI API Key Error

If you see API key error:
1. Get your key from: https://platform.openai.com/api-keys
2. Update `OPENAI_API_KEY` in `.env`
3. Make sure there are no extra spaces or quotes

### Neo4j Connection Refused

If Neo4j connection fails:
1. Wait longer for Neo4j to start (try 60 seconds)
2. Check Neo4j logs: `docker-compose logs neo4j`
3. Verify Neo4j is running: `docker-compose ps`

### Embedding Model Download

First run will download the embedding model (~90MB):
- This is normal and only happens once
- Model is cached in Docker volume
- Subsequent runs will be faster

## 📄 License

MIT License - See LICENSE file for details

