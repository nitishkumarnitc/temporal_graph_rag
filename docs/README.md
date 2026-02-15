# Documentation Index

## 📚 Overview

This folder contains all documentation for the Temporal Knowledge Graph RAG system built with Zep's Graphiti library.

---

## 🚀 Getting Started

### Quick Start
1. **[RUN_ME.md](RUN_ME.md)** - ⭐ **START HERE!** Quick start guide to get the system running
2. **[QUICK_START.md](QUICK_START.md)** - Detailed step-by-step setup and usage guide

### Setup Guides
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Docker and Neo4j container setup
- **[DEPENDENCIES_SETUP.md](DEPENDENCIES_SETUP.md)** - Python dependencies and environment setup
- **[GRAPHITI_SETUP.md](GRAPHITI_SETUP.md)** - Graphiti library setup and configuration

---

## 🎯 Core Features

### Multi-Tenant Data Isolation
- **[TENANT_ISOLATION.md](TENANT_ISOLATION.md)** - Complete guide to multi-tenant data isolation
  - How tenant isolation works using Graphiti's `group_ids`
  - Mandatory tenant context for all queries
  - Preventing cross-tenant data leaks
  - Usage examples and best practices

### Community Detection
- **[COMMUNITY_EXPLANATION.md](COMMUNITY_EXPLANATION.md)** - Understanding community detection in knowledge graphs
  - What communities are and why they matter
  - How Graphiti builds communities automatically
  - Querying community data
  - Use cases and benefits

---

## 🔧 System Architecture

### Key Components
1. **FastAPI Backend** - REST API for data ingestion and search
2. **Graphiti (Zep)** - Temporal knowledge graph framework
3. **Neo4j** - Graph database backend
4. **OpenAI** - LLM and embeddings provider

### Data Flow
```
User Request → FastAPI → Graphiti → Neo4j → Results
                  ↓
              OpenAI LLM
           (Entity Extraction,
            Query Enhancement)
```

---

## 📖 API Endpoints

### Health Check
```bash
GET /health
```

### Ingest Data
```bash
POST /ingest
{
  "data": "string or dict",
  "tenant_id": "string (required)",
  "reference_time": "ISO 8601 timestamp (optional)",
  "context": "string (optional)"
}
```

### Search
```bash
POST /search
{
  "query": "string (required)",
  "tenant_id": "string (required)",
  "num_results": "integer (optional, default: 10)"
}
```

### Export Graph
```bash
POST /export/graphml
{
  "tenant_id": "string (required)"
}
```

---

## 🎓 Learning Path

### For New Users
1. **Start**: [RUN_ME.md](RUN_ME.md) - Get the system running
2. **Learn**: [QUICK_START.md](QUICK_START.md) - Understand how to use it
3. **Explore**: [TENANT_ISOLATION.md](TENANT_ISOLATION.md) - Multi-tenant features
4. **Advanced**: [COMMUNITY_EXPLANATION.md](COMMUNITY_EXPLANATION.md) - Graph communities

### For Developers
1. **Setup**: [GRAPHITI_SETUP.md](GRAPHITI_SETUP.md) - Understand the core library
2. **Architecture**: Review `src/` directory structure
3. **API**: Study `src/api/routes.py` for endpoint implementation
4. **Database**: Review `src/core/database.py` for Graphiti integration

### For System Administrators
1. **Docker**: [DOCKER_SETUP.md](DOCKER_SETUP.md) - Container setup
2. **Dependencies**: [DEPENDENCIES_SETUP.md](DEPENDENCIES_SETUP.md) - Python environment
3. **Configuration**: Review `.env` file for environment variables
4. **Monitoring**: Check API logs and Neo4j browser

---

## 🔍 Quick Reference

### Start the System
```bash
# 1. Start Neo4j
docker start neo4j-graphrag

# 2. Start API
python -m uvicorn src.api.routes:app --host 0.0.0.0 --port 8000
```

### Ingest Data Example
```bash
curl -X POST http://localhost:8000/ingest \
  -H 'Content-Type: application/json' \
  -d '{
    "data": "John Smith joined TechCorp as Senior Engineer on 2024-01-15",
    "tenant_id": "TENANT001",
    "reference_time": "2024-01-15T09:00:00Z",
    "context": "Employee onboarding event"
  }'
```

### Search Example
```bash
curl -X POST http://localhost:8000/search \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "Who joined TechCorp?",
    "tenant_id": "TENANT001",
    "num_results": 10
  }'

---

## 🆘 Troubleshooting

### Neo4j Issues
```bash
# Check if running
docker ps | grep neo4j

# Start if stopped
docker start neo4j-graphrag

# View logs
docker logs neo4j-graphrag

# Access browser
open http://localhost:7474
```

### API Issues
```bash
# Check health
curl http://localhost:8000/health

# View logs (if running in terminal)
# Check for errors in the output

# Restart API
# Ctrl+C to stop, then restart
python -m uvicorn src.api.routes:app --host 0.0.0.0 --port 8000
```

### Common Errors

1. **"Tenant ID required"** - Add `tenant_id` to your request
2. **"No results found"** - Verify `tenant_id` matches between ingest and search
3. **"Connection refused"** - Neo4j is not running, start it with `docker start neo4j-graphrag`
4. **Import errors** - Run `pip install -r requirements.txt`

---

## 📚 External Resources

- **Graphiti (Zep)**: https://github.com/getzep/graphiti
- **Neo4j**: https://neo4j.com/docs/
- **FastAPI**: https://fastapi.tiangolo.com/
- **OpenAI API**: https://platform.openai.com/docs

---

## 📝 Notes

- All customer-specific files (private data/DMS) have been moved to `examples/private data/` (gitignored)
- Documentation focuses on core, reusable features
- System uses OpenAI for LLM and embeddings
- Multi-tenant isolation is mandatory for all operations
- All outdated/redundant documentation has been removed
```

