#!/usr/bin/env python3
"""
General Query Examples for Temporal Knowledge Graph RAG

This script demonstrates how to query the knowledge graph with:
- Tenant context (required for multi-tenant isolation)
- Natural language queries
- Customer/Entity context (optional for enhanced results)

Usage:
    python examples/general_queries.py --tenant-id TENANT001
"""

import argparse
import json
import requests
from typing import Dict, Any, Optional


API_BASE_URL = "http://localhost:8000"


def search(
    query: str,
    tenant_id: str,
    num_results: int = 10,
    customer_id: Optional[str] = None,
    customer_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search the knowledge graph.
    
    Args:
        query: Natural language query
        tenant_id: Tenant identifier (required)
        num_results: Number of results to return
        customer_id: Optional customer/entity ID for context
        customer_name: Optional customer/entity name for context
    
    Returns:
        API response as dictionary
    """
    payload = {
        "query": query,
        "tenant_id": tenant_id,
        "num_results": num_results
    }
    
    # Add customer context if provided
    if customer_id or customer_name:
        payload["customer_context"] = {}
        if customer_id:
            payload["customer_context"]["customer_id"] = customer_id
        if customer_name:
            payload["customer_context"]["customer_name"] = customer_name
    
    response = requests.post(f"{API_BASE_URL}/search", json=payload)
    response.raise_for_status()
    return response.json()


def print_results(query: str, results: Dict[str, Any]):
    """Pretty print search results."""
    print(f"\n{'='*80}")
    print(f"Query: {query}")
    print(f"{'='*80}")
    
    if "results" in results and results["results"]:
        for i, result in enumerate(results["results"][:5], 1):
            # Our API returns "fact" and "name" fields (see SearchService),
            # not "content". Prefer fact, then name, then a JSON fallback.
            primary_text = result.get("fact") or result.get("name")
            if not primary_text:
                primary_text = json.dumps(result, ensure_ascii=False)

            print(f"\n{i}. {primary_text}")

            # Optional extra metadata if present
            if result.get('name') and result.get('name') != primary_text:
                print(f"   Name: {result['name']}")
            if result.get('created_at'):
                print(f"   Created: {result['created_at']}")
            if result.get('score') is not None:
                print(f"   Score: {result['score']:.4f}")
    else:
        print("No results found.")
    
    print(f"\n{'='*80}\n")


def run_example_queries(tenant_id: str):
    """Run example queries demonstrating various scenarios."""
    
    print(f"\n🔍 Running example queries for tenant: {tenant_id}\n")
    
    # Query 1: Employee information
    print("Query 1: Employee information")
    results = search(
        query="Tell me about Sarah Johnson",
        tenant_id=tenant_id,
        num_results=10
    )
    print_results("Tell me about Sarah Johnson", results)
    
    # Query 2: Project information
    print("Query 2: Project information")
    results = search(
        query="What is the Cloud Migration project?",
        tenant_id=tenant_id,
        num_results=10
    )
    print_results("What is the Cloud Migration project?", results)
    
    # Query 3: Customer-specific query with context
    print("Query 3: Customer-specific query with context")
    results = search(
        query="What work was done for Acme Corp?",
        tenant_id=tenant_id,
        num_results=10,
        customer_id="CUST001",
        customer_name="Acme Corp"
    )
    print_results("What work was done for Acme Corp?", results)
    
    # Query 4: Team collaboration
    print("Query 4: Team collaboration")
    results = search(
        query="Who worked with Sarah Johnson?",
        tenant_id=tenant_id,
        num_results=10
    )
    print_results("Who worked with Sarah Johnson?", results)
    
    # Query 5: Temporal query
    print("Query 5: Temporal query")
    results = search(
        query="What happened with Sarah Johnson's career?",
        tenant_id=tenant_id,
        num_results=10
    )
    print_results("What happened with Sarah Johnson's career?", results)
    
    print("✅ All example queries completed!")


def main():
    parser = argparse.ArgumentParser(description="General query examples")
    parser.add_argument("--tenant-id", default="TENANT001", help="Tenant ID for multi-tenant isolation")
    parser.add_argument("--query", help="Custom query to run")
    parser.add_argument("--customer-id", help="Customer ID for context")
    parser.add_argument("--customer-name", help="Customer name for context")
    
    args = parser.parse_args()
    
    try:
        if args.query:
            # Run custom query
            results = search(
                query=args.query,
                tenant_id=args.tenant_id,
                customer_id=args.customer_id,
                customer_name=args.customer_name
            )
            print_results(args.query, results)
        else:
            # Run example queries
            run_example_queries(args.tenant_id)
    
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the server is running:")
        print("   python -m uvicorn src.api.routes:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

