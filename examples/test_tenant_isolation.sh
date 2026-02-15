#!/bin/bash

# Test Tenant Isolation
# This script demonstrates multi-tenant data isolation using tenant_context

echo "================================================================================"
echo "TENANT ISOLATION TEST"
echo "================================================================================"
echo ""

# ==============================================================================
# STEP 1: Ingest data for Tenant 1 (Premium Motors)
# ==============================================================================
echo "🏢 STEP 1: Ingesting data for Tenant 1 (Premium Motors - DEALER001)"
echo "--------------------------------------------------------------------------------"
echo ""

echo "1.1 Adding customer John Anderson to Premium Motors"
curl -X 'POST' 'http://localhost:8000/ingest' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": "John Anderson purchased a BMW X5 from Premium Motors on January 25, 2024. Sale price: $76,000. Sales consultant: Jennifer Lee.",
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
echo -e "\n"

echo "1.2 Adding service record for John Anderson at Premium Motors"
curl -X 'POST' 'http://localhost:8000/ingest' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": "John Anderson brought his BMW X5 to Premium Motors for first service on March 15, 2024. Service included oil change and tire rotation. Service advisor: Lisa Chen.",
  "reference_time": "2024-03-15T09:00:00Z",
  "context": "Service visit",
  "tenant_context": {
    "tenant_id": "DEALER001",
    "tenant_name": "Premium Motors"
  },
  "customer_context": {
    "customer_id": "CUST001",
    "customer_name": "John Anderson"
  }
}'
echo -e "\n"

# ==============================================================================
# STEP 2: Ingest data for Tenant 2 (Valley Auto Group)
# ==============================================================================
echo ""
echo "🏢 STEP 2: Ingesting data for Tenant 2 (Valley Auto Group - DEALER002)"
echo "--------------------------------------------------------------------------------"
echo ""

echo "2.1 Adding customer Sarah Kim to Valley Auto Group"
curl -X 'POST' 'http://localhost:8000/ingest' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": "Sarah Kim purchased a Honda CR-V from Valley Auto Group on February 25, 2024. Sale price: $36,200. Sales consultant: Carlos Martinez.",
  "reference_time": "2024-02-25T14:00:00Z",
  "context": "Vehicle purchase",
  "tenant_context": {
    "tenant_id": "DEALER002",
    "tenant_name": "Valley Auto Group",
    "tenant_address": "456 Valley Blvd, San Jose, CA 95110"
  },
  "customer_context": {
    "customer_id": "CUST002",
    "customer_name": "Sarah Kim",
    "customer_address": "321 Pine St, San Jose, CA 95112"
  }
}'
echo -e "\n"

echo "2.2 Adding service record for Sarah Kim at Valley Auto Group"
curl -X 'POST' 'http://localhost:8000/ingest' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": "Sarah Kim brought her Honda CR-V to Valley Auto Group for first service on April 10, 2024. Service included oil change and inspection. Service advisor: Mike Johnson.",
  "reference_time": "2024-04-10T10:00:00Z",
  "context": "Service visit",
  "tenant_context": {
    "tenant_id": "DEALER002",
    "tenant_name": "Valley Auto Group"
  },
  "customer_context": {
    "customer_id": "CUST002",
    "customer_name": "Sarah Kim"
  }
}'
echo -e "\n"

# ==============================================================================
# STEP 3: Test tenant isolation in queries
# ==============================================================================
echo ""
echo "🔍 STEP 3: Testing Tenant Isolation in Queries"
echo "--------------------------------------------------------------------------------"
echo ""

echo "3.1 Query for John Anderson WITH tenant context (should return only Premium Motors data)"
echo "Expected: Only Premium Motors data"
curl -s -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What did John Anderson do?",
  "num_results": 10,
  "tenant_context": {
    "tenant_id": "DEALER001",
    "tenant_name": "Premium Motors"
  },
  "customer_context": {
    "customer_name": "John Anderson"
  }
}' | python3 -m json.tool | head -50
echo -e "\n"

echo "3.2 Query for Sarah Kim WITH tenant context (should return only Valley Auto Group data)"
echo "Expected: Only Valley Auto Group data"
curl -s -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What did Sarah Kim do?",
  "num_results": 10,
  "tenant_context": {
    "tenant_id": "DEALER002",
    "tenant_name": "Valley Auto Group"
  },
  "customer_context": {
    "customer_name": "Sarah Kim"
  }
}' | python3 -m json.tool | head -50
echo -e "\n"

echo "3.3 Query using tenant_id field directly (should return only Premium Motors data)"
echo "Expected: Only Premium Motors data"
curl -s -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What vehicles were purchased?",
  "num_results": 10,
  "tenant_id": "DEALER001"
}' | python3 -m json.tool | head -50
echo -e "\n"

echo "3.4 Query WITHOUT tenant context (should return data from both tenants)"
echo "Expected: Data from both Premium Motors and Valley Auto Group"
curl -s -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "Who purchased vehicles?",
  "num_results": 10
}' | python3 -m json.tool | head -50
echo -e "\n"

echo "================================================================================"
echo "✅ TENANT ISOLATION TEST COMPLETE"
echo "================================================================================"
echo ""
echo "Review the results above to verify:"
echo "  1. Queries with tenant_context only return data for that tenant"
echo "  2. Queries without tenant_context return data from all tenants"
echo "  3. Data is properly isolated by tenant_id (group_id)"
echo ""

