#!/usr/bin/env bash

# Clear All Data from Neo4j Graph Database
# WARNING: This will delete ALL nodes, relationships, and data!
#
# Usage: bash clear_neo4j.sh

echo "================================================================================"
echo "CLEAR NEO4J DATABASE"
echo "================================================================================"
echo ""
echo "🗑️  Clearing Neo4j database..."
echo ""

# Optional: set DOCKER_HOST if you're using Colima on macOS
# export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"

# Simple method: Delete all nodes and relationships
echo "Step 1: Deleting all nodes and relationships..."
docker exec neo4j-graphrag cypher-shell -u neo4j -p graph_rag \
  "MATCH (n) DETACH DELETE n;"

echo ""
echo "Step 2: Verifying deletion..."
docker exec neo4j-graphrag cypher-shell -u neo4j -p graph_rag \
  "MATCH (n) RETURN count(n) as total_nodes;"

echo ""
echo "✅ Neo4j database cleared!"
echo ""
echo "You can now run:"
echo "  bash run_general_ingestion.sh   # Ingest general data"
echo "  bash run_general_queries.sh     # Query general data"
echo ""

