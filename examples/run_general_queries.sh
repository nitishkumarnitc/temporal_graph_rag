#!/bin/bash

# General Query Examples
# Demonstrates querying with tenant and customer context

echo "🔍 General Query Examples"
echo "========================="
echo ""

# Default tenant ID
TENANT_ID="${1:-TENANT001}"

echo "Tenant ID: $TENANT_ID"
echo ""

# Run the queries
python examples/general_queries.py --tenant-id "$TENANT_ID"

echo ""
echo "✅ Queries complete!"
echo ""
echo "To run a custom query:"
echo "  python examples/general_queries.py --tenant-id $TENANT_ID --query 'your query here'"
echo ""
echo "To add customer context:"
echo "  python examples/general_queries.py --tenant-id $TENANT_ID --customer-id CUST001 --query 'your query'"

