# 🚀 Quick Start: LLM Query Enhancement

## ✨ What's New

**You can now use natural language queries!**

Before:
```bash
"query": "David Chen left TechVision manager Engineering"  # Manual keywords
```

After:
```bash
"query": "What happened to David Chen?"  # Natural language!
```

The LLM automatically enhances your query with entity names and key concepts.

---

## 📋 Step-by-Step Instructions

### Step 1: Start Docker Containers

```bash
cd /Users/nitishkumar/private dataPOCs/graph_rag

# Start containers
docker-compose up --build -d

# Wait 10-15 seconds for services to start

# Check if API is running
curl http://localhost:8000/health
```

**Expected Output**:
```json
{
  "status": "healthy",
  "timestamp": "2024-...",
  "graphiti": "connected"
}
```

---

### Step 2: Clear Database

```bash
cd examples

# Clear all existing data
bash clear_neo4j.sh
```

**Expected Output**:
```
Step 1: Deleting all nodes and relationships...
Step 2: Verifying deletion...
total_nodes
0
✅ Neo4j database cleared!
```

---

### Step 3: Ingest Data

Choose one:

**Option A: General Data** (Recommended)
```bash
bash examples/run_general_ingestion.sh
```

**Option B: Employee Data**
```bash
bash complex_ingestion_queries.sh
```

**Expected**: ~23 episodes ingested, takes 5-10 minutes

---

### Step 4: Test Natural Language Queries

```bash
# Run natural language queries
bash natural_language_queries.sh
```

**What you'll see**:
```
🔍 Query Enhancement:
   Original: What happened to David Chen?
   Enhanced: David Chen departure left manager Engineering

Results: [...]
```

---

## 🧪 Manual Testing

### Test 1: Simple Natural Language Query

```bash
curl -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What happened to David Chen?",
  "num_results": 15,
  "use_entity_filter": true,
  "enhance_query": true
}' | python3 -m json.tool
```

**Check the logs** to see query enhancement:
```bash
docker logs graph-rag-api | tail -20
```

---

### Test 2: Customer Query

```bash
curl -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What car did John Anderson buy?",
  "num_results": 15,
  "enhance_query": true
}' | python3 -m json.tool
```

---

### Test 3: General Query

```bash
curl -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "Tell me about Sarah Johnson",
  "tenant_id": "TENANT001",
  "num_results": 20
}' | python3 -m json.tool
```

---

## 📊 Verify Results

### Check Graph Statistics

```bash
curl http://localhost:8000/stats | python3 -m json.tool
```

**Expected**:
```json
{
  "entities": 50-70,
  "relationships": 100-150,
  "episodes": 23,
  "graph_density": 0.05-0.10
}
```

---

### Check Episodes

```bash
curl http://localhost:8000/episodes?limit=5 | python3 -m json.tool
```

---

### Check Communities

```bash
curl http://localhost:8000/communities | python3 -m json.tool
```

If no communities:
```bash
curl -X POST http://localhost:8000/build-communities
```

---

## 🎯 Query Comparison

### Old Way (Manual Keywords)

```bash
curl -X 'POST' 'http://localhost:8000/search' \
  -d '{
  "query": "David Chen left TechVision manager Engineering",
  "use_entity_filter": true,
  "enhance_query": false
}'
```

### New Way (Natural Language)

```bash
curl -X 'POST' 'http://localhost:8000/search' \
  -d '{
  "query": "What happened to David Chen?",
  "use_entity_filter": true,
  "enhance_query": true
}'
```

**Both produce the same results!** But the new way is much easier.

---

## 🔧 Troubleshooting

### Issue: API not responding

```bash
# Check if containers are running
docker ps | grep graph-rag

# Check API logs
docker logs graph-rag-api

# Restart containers
docker-compose restart
```

---

### Issue: No results found

```bash
# Check if data was ingested
curl http://localhost:8000/stats

# If entities = 0, re-run ingestion
bash examples/run_general_ingestion.sh
```

---

### Issue: Query enhancement not working

```bash
# Check API logs for LLM errors
docker logs graph-rag-api | grep "Query Enhancement"

# Verify OpenAI API key
docker exec graph-rag-api env | grep OPENAI_API_KEY
```

---

## 📚 Documentation

- **[LLM_QUERY_ENHANCEMENT_GUIDE.md](docs/LLM_QUERY_ENHANCEMENT_GUIDE.md)** - Full implementation details
- **[QUERY_PATTERN_EXPLANATION.md](docs/QUERY_PATTERN_EXPLANATION.md)** - Why query patterns differ
- **[QUICK_START.md](docs/QUICK_START.md)** - Original quick start guide

---

## ✅ Success Checklist

- [ ] Docker containers running
- [ ] API health check passes
- [ ] Database cleared
- [ ] Data ingested (~23 episodes)
- [ ] Natural language queries work
- [ ] Query enhancement visible in logs
- [ ] Results are relevant

---

## 🎉 What You Can Do Now

1. ✅ **Ask natural language questions**
   - "What happened to David Chen?"
   - "What car did John Anderson buy?"
   - "Who reports to Sarah Martinez?"

2. ✅ **No manual keyword stuffing**
   - LLM automatically extracts entities
   - No need to write "David Chen left TechVision manager Engineering"

3. ✅ **Better user experience**
   - Customer-facing queries work out of the box
   - More intuitive and user-friendly

4. ✅ **Flexible configuration**
   - Enable/disable query enhancement per query
   - Mix natural language and keyword-rich queries

---

**Ready to test? Run these commands:**

```bash
# 1. Start Docker
docker-compose up --build -d

# 2. Clear DB
cd examples && bash clear_neo4j.sh

# 3. Ingest data
bash examples/run_general_ingestion.sh

# 4. Test queries
bash examples/run_general_queries.sh
```

**Enjoy! 🚀**

