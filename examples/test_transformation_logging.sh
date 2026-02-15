#!/bin/bash

# Test Transformation Logging
# Verifies that transformation metadata is returned in API responses

echo "================================================================================"
echo "TRANSFORMATION LOGGING TEST"
echo "================================================================================"
echo ""
echo "Testing natural language queries with transformation metadata..."
echo ""

# Test 1: Entity-based query (should use entity filter)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1: Entity-based query"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Query: 'What happened to David Chen?'"
echo "Expected: Entity filter (David Chen is entity)"
echo ""

curl -s -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What happened to David Chen?",
  "num_results": 5,
  "tenant_id": "DEALER001"
}' | python3 -c "
import json
import sys
data = json.load(sys.stdin)
print('📊 TRANSFORMATION METADATA:')
print(json.dumps(data.get('transformation', {}), indent=2))
print()
print(f'📈 Results: {data.get(\"num_results\", 0)} found')
"

echo ""
echo ""

# Test 2: Generic question (should use semantic search)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2: Generic question"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Query: 'Who has AWS certifications?'"
echo "Expected: Entity filter (AWS is entity, enhanced to include certification types)"
echo ""

curl -s -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "Who has AWS certifications?",
  "num_results": 5,
  "tenant_id": "DEALER001"
}' | python3 -c "
import json
import sys
data = json.load(sys.stdin)
print('📊 TRANSFORMATION METADATA:')
print(json.dumps(data.get('transformation', {}), indent=2))
print()
print(f'📈 Results: {data.get(\"num_results\", 0)} found')
"

echo ""
echo ""

# Test 3: Multi-entity query (should use entity filter)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3: Multi-entity query"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Query: 'What is the relationship between Sarah Martinez and Alex Kumar?'"
echo "Expected: Entity filter (both are entities)"
echo ""

curl -s -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What is the relationship between Sarah Martinez and Alex Kumar?",
  "num_results": 5,
  "tenant_id": "DEALER001"
}' | python3 -c "
import json
import sys
data = json.load(sys.stdin)
print('📊 TRANSFORMATION METADATA:')
print(json.dumps(data.get('transformation', {}), indent=2))
print()
print(f'📈 Results: {data.get(\"num_results\", 0)} found')
"

echo ""
echo ""

# Test 4: Manual override (force semantic search)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4: Manual override"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Query: 'What happened to David Chen?' (force semantic search)"
echo "Expected: Semantic search (manual override)"
echo ""

curl -s -X 'POST' 'http://localhost:8000/search' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What happened to David Chen?",
  "num_results": 5,
  "use_entity_filter": false,
  "tenant_id": "DEALER001"
}' | python3 -c "
import json
import sys
data = json.load(sys.stdin)
print('📊 TRANSFORMATION METADATA:')
print(json.dumps(data.get('transformation', {}), indent=2))
print()
print(f'📈 Results: {data.get(\"num_results\", 0)} found')
"

echo ""
echo ""
echo "✅ Transformation logging test complete!"
echo ""

