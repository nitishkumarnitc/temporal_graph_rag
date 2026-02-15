#!/usr/bin/env python3
"""
General Data Ingestion Example for Temporal Knowledge Graph RAG

This script demonstrates how to ingest data with:
- Temporal information (reference_time)
- Tenant context (for multi-tenant isolation)
- Customer/Entity context (for enhanced entity matching)

Usage:
    python examples/general_data_ingestion.py --tenant-id TENANT001 --num-events 10
"""

import argparse
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


API_BASE_URL = "http://localhost:8000"


def ingest_event(
    data: str,
    tenant_id: str,
    reference_time: Optional[str] = None,
    context: Optional[str] = None,
    customer_id: Optional[str] = None,
    customer_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Ingest a single event into the knowledge graph.
    
    Args:
        data: The event data (natural language description)
        tenant_id: Tenant identifier for multi-tenant isolation
        reference_time: ISO 8601 timestamp of when the event occurred
        context: Additional context to help with entity extraction
        customer_id: Optional customer/entity ID for enhanced matching
        customer_name: Optional customer/entity name for enhanced matching
    
    Returns:
        API response as dictionary
    """
    payload = {
        "data": data,
        "tenant_id": tenant_id
    }
    
    if reference_time:
        payload["reference_time"] = reference_time
    
    if context:
        payload["context"] = context
    
    # Add customer context if provided
    if customer_id or customer_name:
        payload["customer_context"] = {}
        if customer_id:
            payload["customer_context"]["customer_id"] = customer_id
        if customer_name:
            payload["customer_context"]["customer_name"] = customer_name
    
    response = requests.post(f"{API_BASE_URL}/ingest", json=payload)
    response.raise_for_status()
    return response.json()


def generate_sample_events(tenant_id: str, num_events: int = 10):
    """
    Generate and ingest sample events demonstrating various scenarios.
    
    Args:
        tenant_id: Tenant identifier
        num_events: Number of events to generate
    """
    print(f"\n🚀 Starting data ingestion for tenant: {tenant_id}")
    print(f"📊 Generating {num_events} sample events...\n")
    
    base_time = datetime.now() - timedelta(days=30)
    
    # Example 1: Employee onboarding
    print("Event 1: Employee onboarding...")
    result = ingest_event(
        data="Sarah Johnson joined TechCorp as Senior Software Engineer in the Engineering department",
        tenant_id=tenant_id,
        reference_time=(base_time + timedelta(days=0)).isoformat(),
        context="Employee onboarding event"
    )
    print(f"✅ Ingested: {result.get('message', 'Success')}\n")
    
    # Example 2: Project assignment with customer context
    print("Event 2: Project assignment...")
    result = ingest_event(
        data="Sarah Johnson was assigned to lead the Cloud Migration project for Acme Corp",
        tenant_id=tenant_id,
        reference_time=(base_time + timedelta(days=5)).isoformat(),
        context="Project assignment",
        customer_id="CUST001",
        customer_name="Acme Corp"
    )
    print(f"✅ Ingested: {result.get('message', 'Success')}\n")
    
    # Example 3: Meeting event
    print("Event 3: Team meeting...")
    result = ingest_event(
        data="Sarah Johnson and Michael Chen had a planning meeting to discuss the Cloud Migration architecture",
        tenant_id=tenant_id,
        reference_time=(base_time + timedelta(days=7)).isoformat(),
        context="Team collaboration meeting"
    )
    print(f"✅ Ingested: {result.get('message', 'Success')}\n")
    
    # Example 4: Customer interaction
    print("Event 4: Customer interaction...")
    result = ingest_event(
        data="Michael Chen presented the Cloud Migration proposal to Acme Corp stakeholders",
        tenant_id=tenant_id,
        reference_time=(base_time + timedelta(days=10)).isoformat(),
        context="Customer presentation",
        customer_id="CUST001",
        customer_name="Acme Corp"
    )
    print(f"✅ Ingested: {result.get('message', 'Success')}\n")
    
    # Example 5: Project milestone
    print("Event 5: Project milestone...")
    result = ingest_event(
        data="The Cloud Migration project completed Phase 1 successfully with all deliverables met",
        tenant_id=tenant_id,
        reference_time=(base_time + timedelta(days=20)).isoformat(),
        context="Project milestone achievement"
    )
    print(f"✅ Ingested: {result.get('message', 'Success')}\n")
    
    # Example 6: Employee promotion
    print("Event 6: Employee promotion...")
    result = ingest_event(
        data="Sarah Johnson was promoted to Engineering Manager due to excellent performance on the Cloud Migration project",
        tenant_id=tenant_id,
        reference_time=(base_time + timedelta(days=25)).isoformat(),
        context="Employee promotion event"
    )
    print(f"✅ Ingested: {result.get('message', 'Success')}\n")
    
    print(f"✅ Successfully ingested {6} events for tenant {tenant_id}")
    print(f"\n💡 You can now query this data using:")
    print(f"   python examples/general_queries.py --tenant-id {tenant_id}")


def main():
    parser = argparse.ArgumentParser(description="General data ingestion example")
    parser.add_argument("--tenant-id", default="TENANT001", help="Tenant ID for multi-tenant isolation")
    parser.add_argument("--num-events", type=int, default=6, help="Number of events to generate")
    
    args = parser.parse_args()
    
    try:
        generate_sample_events(args.tenant_id, args.num_events)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the server is running:")
        print("   python -m uvicorn src.api.routes:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

