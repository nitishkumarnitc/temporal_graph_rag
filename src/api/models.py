"""Pydantic models for API"""
from typing import Optional, Dict, Any, Union, List
from pydantic import BaseModel, Field


class TenantContext(BaseModel):
	"""Tenant context for multi-tenant isolation"""
	tenant_id: str = Field(..., description="Tenant ID (e.g., 'TENANT001') - Required for isolation")
	tenant_name: Optional[str] = Field(None, description="Tenant name (e.g., 'Premium Org')")
	tenant_address: Optional[str] = Field(None, description="Tenant address")


class CustomerContext(BaseModel):
    """Customer context for enhanced entity matching"""
    customer_id: Optional[str] = Field(None, description="Customer ID (e.g., 'CUST001')")
    customer_name: Optional[str] = Field(None, description="Customer name (e.g., 'John Anderson')")
    customer_address: Optional[str] = Field(None, description="Customer address")


class DataIngestion(BaseModel):
    """Schema-less data ingestion model"""
    data: Union[str, Dict[str, Any], List[Any]] = Field(
        ...,
        description="Raw data in any format: text, JSON object, or array"
    )
    reference_time: Optional[str] = Field(
        None,
        description="Optional: ISO 8601 timestamp when event occurred. If not provided, uses current time"
    )
    context: Optional[str] = Field(
        None,
        description="Optional: Additional context to help with entity extraction"
    )
    tenant_id: Optional[str] = Field(
        None,
        description="Optional: Tenant ID for multi-tenant isolation (alternative to tenant_context)"
    )
    tenant_context: Optional[TenantContext] = Field(
        None,
	    description="Optional: Tenant context for multi-tenant isolation"
    )
    customer_context: Optional[CustomerContext] = Field(
        None,
        description="Optional: Customer context for enhanced entity matching"
    )


class SearchQuery(BaseModel):
    """Search query model"""
    query: str = Field(..., description="Search query text (natural language)")
    num_results: int = Field(default=5, ge=1, le=20, description="Number of results to return")
    group_ids: Optional[List[str]] = Field(None, description="Optional group IDs to filter by (auto-populated from tenant_id/tenant_context if not provided)")
    min_score: float = Field(default=0.7, ge=0.0, le=1.0, description="Minimum similarity score threshold (0.0-1.0). Higher values = more relevant results.")
    use_entity_filter: Optional[bool] = Field(default=None, description="Strategy override: None=auto-detect, True=entity filter (precision), False=semantic search (recall)")
    enhance_query: bool = Field(default=True, description="If True, use LLM to automatically enhance natural language query with entity names and key concepts")
    tenant_id: Optional[str] = Field(
        None,
        description="Tenant ID for filtering (alternative to tenant_context) - REQUIRED for multi-tenant isolation"
    )
    tenant_context: Optional[TenantContext] = Field(
        None,
	    description="Tenant context for multi-tenant isolation - REQUIRED (alternative: use tenant_id field)"
    )
    customer_context: Optional[CustomerContext] = Field(
        None,
        description="Optional: Customer context for enhanced entity matching"
    )

