#!/bin/bash

# Check for Communities in Neo4j Graph
# This script checks if community detection has run and shows community structure
#
# Usage: bash check_communities.sh

echo "================================================================================"
echo "CHECK COMMUNITIES IN NEO4J GRAPH"
echo "================================================================================"
echo ""

# Set Docker host for Colima
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"

echo "📊 Checking graph statistics..."
echo ""

# Count total nodes
echo "1. Total Nodes:"
docker exec neo4j-graphrag cypher-shell -u neo4j -p graph_rag \
  "MATCH (n) RETURN labels(n)[0] as type, count(*) as count ORDER BY count DESC;"

echo ""
echo "2. Total Relationships:"
docker exec neo4j-graphrag cypher-shell -u neo4j -p graph_rag \
  "MATCH ()-[r]->() RETURN type(r) as relationship_type, count(*) as count ORDER BY count DESC LIMIT 10;"

echo ""
echo "3. Community Nodes:"
docker exec neo4j-graphrag cypher-shell -u neo4j -p graph_rag \
  "MATCH (c:Community) RETURN c.name as community_name, c.summary as summary, c.size as size LIMIT 10;"

COMMUNITY_COUNT=$(docker exec neo4j-graphrag cypher-shell -u neo4j -p graph_rag \
  "MATCH (c:Community) RETURN count(c) as count;" | grep -oE '[0-9]+' | head -1)

echo ""
if [ "$COMMUNITY_COUNT" -eq "0" ] || [ -z "$COMMUNITY_COUNT" ]; then
    echo "⚠️  No communities found!"
    echo ""
    echo "Possible reasons:"
    echo "  1. Not enough data ingested (need 50+ entities)"
    echo "  2. Community detection hasn't run yet (asynchronous process)"
    echo "  3. Community detection is disabled in configuration"
    echo ""
    echo "To manually trigger community building:"
    echo "  1. Use the API endpoint: POST /build-communities"
    echo "  2. Or run: curl -X POST http://localhost:8000/build-communities"
    echo ""
else
    echo "✅ Found $COMMUNITY_COUNT communities!"
    echo ""
    echo "4. Community Membership:"
    docker exec neo4j-graphrag cypher-shell -u neo4j -p graph_rag \
      "MATCH (e:Entity)-[:BELONGS_TO]->(c:Community) RETURN c.name as community, e.name as entity LIMIT 20;"
fi

echo ""
echo "5. Sample Entities:"
docker exec neo4j-graphrag cypher-shell -u neo4j -p graph_rag \
  "MATCH (e:Entity) RETURN e.name as entity_name, e.entity_type as type LIMIT 10;"

echo ""
echo "6. Sample Relationships (Edges):"
docker exec neo4j-graphrag cypher-shell -u neo4j -p graph_rag \
  "MATCH (s:Entity)-[r]->(t:Entity) RETURN s.name as source, type(r) as relationship, t.name as target LIMIT 10;"

echo ""
echo "================================================================================"
echo "COMMUNITY DETECTION STATUS"
echo "================================================================================"
echo ""

if [ "$COMMUNITY_COUNT" -eq "0" ] || [ -z "$COMMUNITY_COUNT" ]; then
    echo "Status: ❌ Communities NOT detected"
    echo ""
    echo "Next steps:"
    echo "  1. Ensure you have ingested enough data (50+ entities recommended)"
    echo "  2. Wait a few minutes for background processing"
    echo "  3. Manually trigger: curl -X POST http://localhost:8000/build-communities"
    echo "  4. Re-run this script to verify"
else
    echo "Status: ✅ Communities detected and built"
    echo ""
    echo "You can now query communities through the search API!"
fi

echo ""

