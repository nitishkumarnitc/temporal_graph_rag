# Examples

This folder contains example scripts demonstrating how to use the Temporal Knowledge Graph RAG system.

## 📁 General Examples (Recommended)

### Data Ingestion
- **`general_data_ingestion.py`** - Python script demonstrating data ingestion with:
  - Temporal information (`reference_time`)
  - Tenant context (for multi-tenant isolation)
  - Customer/Entity context (for enhanced entity matching)
  
- **`run_general_ingestion.sh`** - Shell wrapper for easy execution

**Usage:**
```bash
# Using shell script (recommended)
bash examples/run_general_ingestion.sh

# Using Python directly
python examples/general_data_ingestion.py --tenant-id TENANT001 --num-events 6

# Custom tenant
python examples/general_data_ingestion.py --tenant-id MYORG --num-events 10
```

### Querying
- **`general_queries.py`** - Python script demonstrating queries with:
  - Natural language queries
  - Tenant context (required)
  - Customer/Entity context (optional)
  
- **`run_general_queries.sh`** - Shell wrapper for easy execution

**Usage:**
```bash
# Run example queries
bash examples/run_general_queries.sh

# Custom query
python examples/general_queries.py --tenant-id TENANT001 --query "Tell me about Sarah Johnson"

# Query with customer context
python examples/general_queries.py \
  --tenant-id TENANT001 \
  --customer-id CUST001 \
  --customer-name "Acme Corp" \
  --query "What work was done for this customer?"
```

---

## 🛠️ Utility Scripts

### Clear Neo4j Database
- **`clear_neo4j.sh`** - Clears all data from Neo4j database

**Usage:**
```bash
bash examples/clear_neo4j.sh
```

### Check Communities
- **`check_communities.sh`** - Checks if community detection has run

**Usage:**
```bash
bash examples/check_communities.sh
```

### Test Tenant Isolation
- **`test_tenant_isolation.sh`** - Tests multi-tenant data isolation

**Usage:**
```bash
bash examples/test_tenant_isolation.sh
```

---

## 📚 Key Concepts

### Temporal Information
All events should include a `reference_time` (ISO 8601 timestamp) indicating when the event occurred:
```python
reference_time="2024-01-15T09:00:00Z"
```

### Tenant Context (Required)
Every ingestion and query must include a `tenant_id` for multi-tenant isolation:
```python
tenant_id="TENANT001"
```

### Customer Context (Optional)
Optionally include customer/entity information for enhanced entity matching:
```python
customer_context={
    "customer_id": "CUST001",
    "customer_name": "Acme Corp"
}
```

---

## 🎯 Quick Start

1. **Start the system:**
   ```bash
   # Start Neo4j
   docker start neo4j-graphrag
   
   # Start API
   python -m uvicorn src.api.routes:app --host 0.0.0.0 --port 8000
   ```

2. **Ingest sample data:**
   ```bash
   bash examples/run_general_ingestion.sh
   ```

3. **Run queries:**
   ```bash
   bash examples/run_general_queries.sh
   ```

4. **View in Neo4j browser:**
   ```
   http://localhost:7474
   ```

---

## 📝 Notes
- These general examples demonstrate core features applicable to any domain
- Examples use realistic but generic data (employees, projects, customers)

