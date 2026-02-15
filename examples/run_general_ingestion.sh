#!/bin/bash

# General Data Ingestion Example
# Demonstrates ingestion with temporal, tenant, and customer context

echo "🚀 General Data Ingestion Example"
echo "=================================="
echo ""
echo "This script demonstrates how to ingest data with:"
echo "  - Temporal information (reference_time)"
echo "  - Tenant context (for multi-tenant isolation)"
echo "  - Customer/Entity context (for enhanced entity matching)"
echo ""

# Default tenant ID
TENANT_ID="${1:-TENANT001}"
NUM_EVENTS="${2:-6}"

echo "Tenant ID: $TENANT_ID"
echo "Number of events: $NUM_EVENTS"
echo ""

# Run the ingestion
python -u examples/general_data_ingestion.py \
  --tenant-id "$TENANT_ID" \
  --num-events "$NUM_EVENTS"

echo ""
echo "✅ Ingestion complete!"
echo ""
echo "Next steps:"
echo "  1. Run queries: bash examples/run_general_queries.sh $TENANT_ID"
echo "  2. View in Neo4j browser: http://localhost:7474"
echo "  3. Run custom query: python examples/general_queries.py --tenant-id $TENANT_ID --query 'your query here'"

