# Quick Start Guide - Temporal Knowledge Graph

## 🚀 Complete Workflow

### Prerequisites
- Docker containers running: `graph-rag-api` and `neo4j-graphrag`
- API accessible at `http://localhost:8000`

---

## Step-by-Step Instructions

### 1️⃣ Restart API (Apply Community Building Changes)

```bash
cd /Users/nitishkumar/private dataPOCs/graph_rag

# Stop containers
docker-compose down

# Rebuild and start
docker-compose up --build -d

# Check API is running
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

### 2️⃣ Clear Existing Data

```bash
cd examples
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

### 3️⃣ Ingest Sample Data

```bash
bash examples/run_general_ingestion.sh
```

**What This Does**:
- Creates sample organization data (TechCorp)
- Ingests employee journeys and project events
- Demonstrates temporal, tenant, and customer context
- Total: 6 ingestion events

**Expected Output**:
```
🚀 Starting data ingestion for tenant: TENANT001
📊 Generating 6 sample events...

Event 1: Employee onboarding...
✅ Ingested: Success

Event 2: Project assignment...
✅ Ingested: Success

✅ Successfully ingested 6 events for tenant TENANT001
Total Events: ~23 ingestion calls
Expected Entities: 50-70 nodes
Expected Relationships: 100-150 edges
```

**Time**: ~5-10 minutes (depends on LLM processing)

---

### 4️⃣ Verify Data Ingestion

```bash
# Check graph statistics
curl http://localhost:8000/stats | python3 -m json.tool
```

**Expected Output**:
```json
{
  "entities": 50-70,
  "relationships": 100-150,
  "episodes": 23,
  "graph_density": 0.05-0.10
}
```

---

### 5️⃣ Check for Communities

```bash
bash check_communities.sh
```

**Expected Output**:
```
📊 Checking graph statistics...

1. Total Nodes:
type         | count
-------------|------
Entity       | 65
Episodic     | 23
Community    | 4

3. Community Nodes:
community_name                    | summary                          | size
----------------------------------|----------------------------------|-----
Premium Motors Operations         | Sales team and customers...      | 15
Valley Auto Group Operations      | Dealership staff and leads...    | 12
...

✅ Found 4 communities!
```

**If No Communities**:
```bash
# Manually trigger community building
curl -X POST http://localhost:8000/build-communities | python3 -m json.tool
```

---

### 6️⃣ Run Queries

```bash
bash examples/run_general_queries.sh
```

**What This Does**:
- Runs 5 example queries
- Tests natural language query processing
- Queries employee information, projects, and customer interactions

**Sample Queries**:

**Q1: John Anderson's Journey**
```bash
curl -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "John Anderson lead purchase BMW X5 Premium Motors",
  "num_results": 25,
  "use_entity_filter": true
}' | python3 -m json.tool
```

**Expected**: 15-25 results covering lead → test drive → purchase → service

---

## 🔍 Verification Checklist

After completing all steps, verify:

- [ ] API is running (`curl http://localhost:8000/health`)
- [ ] Data ingested (~23 episodes, 50-70 entities)
- [ ] Communities detected (3-5 communities)
- [ ] Queries return relevant results (80%+ precision)

---

## 🛠️ Troubleshooting

### Issue: No Communities Found

**Solution 1**: Wait a few minutes (community detection is asynchronous)

**Solution 2**: Manually trigger
```bash
curl -X POST http://localhost:8000/build-communities
```

**Solution 3**: Check if enough data
```bash
curl http://localhost:8000/stats
# Need at least 30-50 entities
```

---

### Issue: Queries Return No Results

**Check 1**: Verify data was ingested
```bash
curl http://localhost:8000/episodes?limit=5
```

**Check 2**: Try without entity filter
```bash
curl -X 'POST' 'http://localhost:8000/search' \
  -d '{"query": "BMW", "num_results": 10, "use_entity_filter": false}'
```

---

### Issue: API Not Responding

**Check containers**:
```bash
docker ps | grep graph-rag
```

**Check logs**:
```bash
docker logs graph-rag-api
docker logs neo4j-graphrag
```

**Restart**:
```bash
docker-compose restart
```

---

## 📚 Additional Resources

- **Full Documentation**: `examples/README.md`
- **Community Explanation**: `examples/COMMUNITY_EXPLANATION.md`
- **Changes Made**: `CHANGES.md`
- **API Docs**: http://localhost:8000/docs

---

## 🎯 Quick Commands Reference

```bash
# Restart API
docker-compose down && docker-compose up --build -d

# Clear data
bash examples/clear_neo4j.sh

# Ingest data
bash examples/run_general_ingestion.sh

# Check communities
bash examples/check_communities.sh

# Run queries
bash examples/run_general_queries.sh

# Manual community build
curl -X POST http://localhost:8000/build-communities

# List communities
curl http://localhost:8000/communities
```

