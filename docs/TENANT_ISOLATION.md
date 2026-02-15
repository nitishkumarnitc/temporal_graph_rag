# Multi-Tenant Isolation Guide

## Overview

The Temporal Knowledge Graph RAG system now supports **multi-tenant data isolation** using tenant context. This ensures that data from different tenants (e.g., companies, organizations) is properly isolated and queries only return data for the specified tenant.

---

## Key Concepts

### Tenant Context vs Customer Context

The system separates tenant and customer information into two distinct contexts:

- **Tenant Context** (`tenant_context`): Organization details (ID, name, address)
  - Used for **data isolation** via `group_id`
  - Required field: `tenant_id`

- **Customer Context** (`customer_context`): Customer details (ID, name, address)
  - Used for **enhanced entity matching** in queries
  - All fields optional

- **Tenant ID Field** (`tenant_id`): Shorthand for simple tenant isolation
  - Alternative to full `tenant_context` object
  - Just provide the tenant ID as a string

### How It Works

1. **Data Ingestion**: When ingesting data, include `tenant_context` in the request
2. **Automatic Isolation**: System automatically assigns `group_id` from `tenant_id`
3. **Query Filtering**: Queries with `tenant_context` only return data for that tenant
4. **Data Separation**: Each tenant's data is stored with a unique `group_id` in Neo4j

---

## API Models

### TenantContext Model

```python
{
  "tenant_id": "DEALER001",           # Required
  "tenant_name": "Premium Motors",    # Optional
  "tenant_address": "123 Main St"     # Optional
}
```

| Field | Required | Purpose |
|-------|----------|---------|
| `tenant_id` | **Yes** | Unique identifier for tenant (used as `group_id` for isolation) |
| `tenant_name` | No | Organization name (enhances entity matching in queries) |
| `tenant_address` | No | Organization address |

### CustomerContext Model

```python
{
  "customer_id": "CUST001",           # Optional
  "customer_name": "John Anderson",   # Optional
  "customer_address": "456 Oak St"    # Optional
}
```

| Field | Required | Purpose |
|-------|----------|---------|
| `customer_id` | No | Customer identifier |
| `customer_name` | No | Customer name (enhances entity matching in queries) |
| `customer_address` | No | Customer address |

### Tenant ID Field (Shorthand)

You can also use just the `tenant_id` field directly instead of the full `tenant_context` object:

```python
{
  "tenant_id": "DEALER001"  # Simple string field
}
```

---

## Usage Examples

### 1. Data Ingestion with Full Context

```bash
curl -X 'POST' 'http://localhost:8000/ingest' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": "John Anderson purchased a BMW X5 from Premium Motors on January 25, 2024.",
  "reference_time": "2024-01-25T16:00:00Z",
  "context": "Vehicle purchase",
  "tenant_context": {
    "tenant_id": "DEALER001",
    "tenant_name": "Premium Motors",
    "tenant_address": "123 Luxury Ave, San Francisco, CA 94102"
  },
  "customer_context": {
    "customer_id": "CUST001",
    "customer_name": "John Anderson",
    "customer_address": "789 Oak St, San Francisco, CA 94117"
  }
}'
```

**What Happens Internally:**
1. System extracts `tenant_id` = "DEALER001" from `tenant_context`
2. Sets `group_id` = "DEALER001" in Graphiti
3. Adds tenant and customer context to episode description
4. All entities/relationships are tagged with `group_id`

### 1b. Data Ingestion with Tenant ID Only (Shorthand)

```bash
curl -X 'POST' 'http://localhost:8000/ingest' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": "John Anderson purchased a BMW X5 from Premium Motors on January 25, 2024.",
  "reference_time": "2024-01-25T16:00:00Z",
  "context": "Vehicle purchase",
  "tenant_id": "DEALER001",
  "customer_context": {
    "customer_name": "John Anderson"
  }
}'
```

**What Happens Internally:**
1. System uses `tenant_id` = "DEALER001" directly
2. Sets `group_id` = "DEALER001" in Graphiti
3. Adds customer context to episode description

### 2. Search with Full Context (Isolated Query)

```bash
curl -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What did John Anderson purchase?",
  "num_results": 10,
  "tenant_context": {
    "tenant_id": "DEALER001",
    "tenant_name": "Premium Motors"
  },
  "customer_context": {
    "customer_name": "John Anderson"
  }
}'
```

**What Happens Internally:**
1. System extracts `tenant_id` = "DEALER001" from `tenant_context`
2. Auto-populates `group_ids` = ["DEALER001"]
3. Enhances query with customer name ("John Anderson") and tenant name ("Premium Motors")
4. Filters results to only include data with `group_id` = "DEALER001"

**Response:**
```json
{
  "query": "What did John Anderson purchase?",
  "num_results": 2,
  "tenant_id": null,
  "tenant_context": {
    "tenant_id": "DEALER001",
    "tenant_name": "Premium Motors"
  },
  "customer_context": {
    "customer_name": "John Anderson"
  },
  "group_ids": ["DEALER001"],
  "transformation": { ... },
  "results": [ ... ]  // Only Premium Motors data
}
```

### 2b. Search with Tenant ID Only (Shorthand)

```bash
curl -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What vehicles were purchased?",
  "num_results": 10,
  "tenant_id": "DEALER001"
}'
```

**What Happens Internally:**
1. System uses `tenant_id` = "DEALER001" directly
2. Auto-populates `group_ids` = ["DEALER001"]
3. Filters results to only include data with `group_id` = "DEALER001"

### 3. Search without Tenant Context (All Data)

```bash
curl -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "Who purchased vehicles?",
  "num_results": 10
}'
```

**Result**: Returns data from **all tenants** (no filtering)

---

## Benefits

### 1. **Data Isolation**
- Each tenant's data is completely isolated
- No risk of data leakage between tenants
- Queries automatically filtered by tenant

### 2. **Better Entity Matching**
- Customer/tenant names enhance query understanding
- LLM can better identify relevant entities
- More accurate search results

### 3. **Flexible Querying**
- Query specific tenant data (with `tenant_context`)
- Query all data (without `tenant_context`)
- Override with manual `group_ids` if needed

### 4. **Audit Trail**
- Every ingestion includes tenant information
- Easy to track which tenant owns which data
- Supports compliance and data governance

---

## Testing Tenant Isolation

Run the tenant isolation test script:

```bash
cd graph_rag/examples
bash test_tenant_isolation.sh
```

This script:
1. Ingests data for Tenant 1 (Premium Motors)
2. Ingests data for Tenant 2 (Valley Auto Group)
3. Queries with tenant context (should return only that tenant's data)
4. Queries without tenant context (should return all data)

---

## Implementation Details

### Backend Changes

1. **`src/api/models.py`**: Added `TenantContext` model
2. **`src/api/routes.py`**: 
   - `/ingest` endpoint extracts tenant context and sets `group_ids`
   - `/search` endpoint auto-populates `group_ids` from `tenant_context`
3. **`src/services/ingestion.py`**: Updated to accept and use `group_ids`

### Neo4j Storage

Data is stored with `group_id` property:
```cypher
// Entities with group_id
MATCH (e:Entity {group_id: "DEALER001"})
RETURN e.name, e.group_id

// Episodes with group_id
MATCH (ep:Episode {group_id: "DEALER001"})
RETURN ep.name, ep.group_id
```

---

## Best Practices

1. **Always include `tenant_id`** for multi-tenant applications
2. **Include customer/tenant names** for better entity matching
3. **Test isolation** before deploying to production
4. **Use consistent tenant IDs** across your system
5. **Document tenant ID format** (e.g., "DEALER001", "DEALER002")

---

## Next Steps

- Update all example scripts to include `tenant_context`
- Test with real multi-tenant data
- Monitor query performance with tenant filtering
- Consider adding tenant-level analytics

