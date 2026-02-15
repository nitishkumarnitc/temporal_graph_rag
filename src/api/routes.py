"""FastAPI routes for Temporal Knowledge Graph RAG"""
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from .models import DataIngestion, SearchQuery
from src.core import get_graphiti_instance, close_graphiti_instance, Config
from src.services import DataIngestionService, SearchService, ExportService


# Global instance
graphiti_instance = None
ingestion_service = None
search_service = None
export_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management for FastAPI"""
    global graphiti_instance, ingestion_service, search_service, export_service
    
    print("🚀 Starting Temporal Knowledge Graph RAG API...")
    
    try:
        # Initialize Graphiti
        graphiti_instance = get_graphiti_instance()
        
        # Initialize services
        ingestion_service = DataIngestionService(graphiti_instance)
        search_service = SearchService(graphiti_instance)
        export_service = ExportService(graphiti_instance)
        
        print("✅ API initialized successfully")
        
        yield
        
    finally:
        print("🛑 Shutting down API...")
        await close_graphiti_instance()
        print("✅ Shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="Temporal Knowledge Graph RAG API",
        description="Schema-less temporal knowledge graph with runtime entity extraction",
        version=Config.API_VERSION,
        lifespan=lifespan
    )
    
    @app.get("/")
    async def root():
        """Root endpoint - API information"""
        return {
            "name": "Temporal Knowledge Graph RAG API",
            "version": Config.API_VERSION,
            "description": "Schema-less temporal knowledge graph with bi-temporal model",
            "endpoints": {
                "health": "/health",
                "ingest": "/ingest",
                "search": "/search",
                "episodes": "/episodes",
                "entities": "/entities",
                "stats": "/stats",
                "build_communities": "/build-communities",
                "communities": "/communities"
            }
        }
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "graphiti": "connected" if graphiti_instance else "disconnected"
        }
    
    @app.post("/ingest", status_code=201)
    async def ingest_data(ingestion: DataIngestion):
        """Schema-less data ingestion - extracts entities/relationships on-the-fly"""
        if not ingestion_service:
            raise HTTPException(status_code=503, detail="Service not initialized")

        try:
            # Parse reference time if provided
            ref_time = None
            if ingestion.reference_time:
                ref_time = datetime.fromisoformat(ingestion.reference_time.replace('Z', '+00:00'))

            # Build context with tenant and customer information
            context_parts = []
            if ingestion.context:
                context_parts.append(ingestion.context)

            # Add tenant context if provided
            if ingestion.tenant_context:
                tc = ingestion.tenant_context
                context_parts.append(f"Tenant ID: {tc.tenant_id}")
                if tc.tenant_name:
                    context_parts.append(f"Tenant Name: {tc.tenant_name}")
                if tc.tenant_address:
                    context_parts.append(f"Tenant Address: {tc.tenant_address}")

            # Add customer context if provided
            if ingestion.customer_context:
                cc = ingestion.customer_context
                if cc.customer_id:
                    context_parts.append(f"Customer ID: {cc.customer_id}")
                if cc.customer_name:
                    context_parts.append(f"Customer: {cc.customer_name}")
                if cc.customer_address:
                    context_parts.append(f"Customer Address: {cc.customer_address}")

            full_context = ". ".join(context_parts) if context_parts else None

            # Determine group_ids for tenant isolation
            # Priority: tenant_context.tenant_id > tenant_id field
            group_ids = []
            if ingestion.tenant_context:
                group_ids.append(ingestion.tenant_context.tenant_id)
            elif ingestion.tenant_id:
                group_ids.append(ingestion.tenant_id)

            # Ingest data with tenant context
            result = await ingestion_service.ingest_data(
                data=ingestion.data,
                reference_time=ref_time,
                context=full_context,
                group_ids=group_ids if group_ids else None
            )

            return result
            
        except Exception as e:
            error_msg = str(e)
            
            # Handle rate limit errors
            if any(x in error_msg.lower() for x in ['rate limit', 'quota', 'too many requests']):
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate Limit Exceeded",
                        "message": error_msg,
                        "suggestion": "Please wait a moment and try again. If you continue to see rate limit errors, reduce request frequency or batch size, or review your OpenAI rate limits.",
                        "original_error": error_msg
                    }
                )
            
            # Handle authentication errors
            if any(x in error_msg.lower() for x in ['authentication', 'api key', 'unauthorized']):
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "Authentication Error",
                        "message": "Invalid or missing OpenAI API key",
                        "suggestion": "Check your OPENAI_API_KEY in the .env file or environment variables.",
                        "original_error": error_msg
                    }
                )
            
            # Handle timeout errors
            if any(x in error_msg.lower() for x in ['timeout', 'timed out']):
                return JSONResponse(
                    status_code=504,
                    content={
                        "error": "Timeout Error",
                        "message": "Request timed out",
                        "suggestion": "Try with smaller data or retry later",
                        "original_error": error_msg
                    }
                )
            
            # Generic error
            raise HTTPException(status_code=500, detail=f"Ingestion failed: {error_msg}")
    
    @app.post("/search")
    async def search(query: SearchQuery):
        """Semantic search with LLM query enhancement and entity-based filtering.

        Note: Tenant context is optional here to support single-tenant/demo usage
        and to align with the test suite. When tenant information is provided,
        it is translated into group_ids for isolation; otherwise the search is
        performed over all data.
        """
        if not search_service:
            raise HTTPException(status_code=503, detail="Service not initialized")

        try:
            # Determine group_ids for tenant isolation (optional)
            # Priority: explicit group_ids > tenant_context.tenant_id > tenant_id field
            group_ids = query.group_ids
            if not group_ids:
                if query.tenant_context:
                    group_ids = [query.tenant_context.tenant_id]
                    print(f"🏢 Tenant isolation: Filtering by tenant_id={query.tenant_context.tenant_id}")
                elif query.tenant_id:
                    group_ids = [query.tenant_id]
                    print(f"🏢 Tenant isolation: Filtering by tenant_id={query.tenant_id}")

            # Enhance query with customer and tenant context if provided
            enhanced_query = query.query
            context_hints = []

            # Add customer context hints
            if query.customer_context and query.customer_context.customer_name:
                context_hints.append(query.customer_context.customer_name)

            # Add tenant context hints
            if query.tenant_context and query.tenant_context.tenant_name:
                context_hints.append(query.tenant_context.tenant_name)

            # Add context hints to query for better entity matching
            if context_hints and query.enhance_query:
                enhanced_query = f"{query.query} {' '.join(context_hints)}"
                print(f"🔍 Enhanced query with context: {enhanced_query}")

            search_result = await search_service.search(
                query=enhanced_query,
                num_results=query.num_results,
                group_ids=group_ids,
                min_score=query.min_score,
                use_entity_filter=query.use_entity_filter,
                enhance_query=query.enhance_query
            )

            # Extract transformation metadata and results
            transformation = search_result.get("transformation", {})
            results = search_result.get("results", [])

            return {
                "query": query.query,
                "num_results": len(results),
                "min_score": query.min_score,
                "tenant_id": query.tenant_id,
                "tenant_context": query.tenant_context.dict() if query.tenant_context else None,
                "customer_context": query.customer_context.dict() if query.customer_context else None,
                "group_ids": group_ids,
                "transformation": transformation,
                "results": results
            }

        except HTTPException:
            # Preserve explicit HTTP errors
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    @app.get("/stats")
    async def get_statistics():
        """Get graph statistics"""
        if not search_service:
            raise HTTPException(status_code=503, detail="Service not initialized")

        try:
            stats = await search_service.get_statistics()
            return stats
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

    @app.get("/entities/{entity_uuid}")
    async def get_entity(entity_uuid: str):
        """Get entity by UUID with relationships"""
        if not search_service:
            raise HTTPException(status_code=503, detail="Service not initialized")

        try:
            entity = await search_service.get_entity(entity_uuid)
            if not entity:
                raise HTTPException(status_code=404, detail="Entity not found")
            return entity
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get entity: {str(e)}")

    @app.get("/entities")
    async def list_entities(
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0)
    ):
        """List entities with basic metadata for inspection.

        Used by tests to validate that semantic entity extraction is working.
        """
        if not graphiti_instance:
            raise HTTPException(status_code=503, detail="Service not initialized")

        try:
            query = """
            MATCH (e:Entity)
            RETURN e.uuid AS uuid,
                   e.name AS name,
                   e.created_at AS created_at,
                   e.valid_at AS valid_at,
                   e.expired_at AS expired_at
            ORDER BY e.created_at DESC
            SKIP $offset
            LIMIT $limit
            """

            async with graphiti_instance.driver.session() as session:
                result = await session.run(query, offset=offset, limit=limit)
                entities = await result.data()

            # Normalize temporal fields to ISO strings if they are temporal objects
            normalized_entities = []
            for ent in entities:
                normalized_entities.append({
                    "uuid": ent.get("uuid"),
                    "name": ent.get("name"),
                    "created_at": ent.get("created_at").isoformat() if hasattr(ent.get("created_at"), "isoformat") and ent.get("created_at") else ent.get("created_at"),
                    "valid_at": ent.get("valid_at").isoformat() if hasattr(ent.get("valid_at"), "isoformat") and ent.get("valid_at") else ent.get("valid_at"),
                    "expired_at": ent.get("expired_at").isoformat() if hasattr(ent.get("expired_at"), "isoformat") and ent.get("expired_at") else ent.get("expired_at"),
                })

            return {
                "total": len(normalized_entities),
                "offset": offset,
                "limit": limit,
                "entities": normalized_entities,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list entities: {str(e)}")

    @app.get("/episodes")
    async def list_episodes(
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0)
    ):
        """List all episodes with pagination"""
        if not graphiti_instance:
            raise HTTPException(status_code=503, detail="Service not initialized")

        try:
            query = f"""
            MATCH (e:Episodic)
            RETURN e.uuid AS uuid, e.name AS name, e.content AS content,
                   e.created_at AS created_at, e.valid_at AS valid_at,
                   e.source AS source
            ORDER BY e.created_at DESC
            SKIP {offset}
            LIMIT {limit}
            """

            async with graphiti_instance.driver.session() as session:
                result = await session.run(query)
                episodes = await result.data()

            return {
                "total": len(episodes),
                "offset": offset,
                "limit": limit,
                "episodes": episodes
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list episodes: {str(e)}")

    @app.post("/build-communities")
    async def build_communities():
        """Manually trigger community detection"""
        if not graphiti_instance:
            raise HTTPException(status_code=503, detail="Service not initialized")

        try:
            print("🔍 Building communities...")
            await graphiti_instance.build_communities()

            # Count communities
            query = "MATCH (c:Community) RETURN count(c) as count"
            async with graphiti_instance.driver.session() as session:
                result = await session.run(query)
                record = await result.single()
                community_count = record['count'] if record else 0

            return {
                "status": "success",
                "message": "Community detection completed",
                "communities_found": community_count
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to build communities: {str(e)}")

    @app.get("/communities")
    async def list_communities(
        limit: int = Query(default=20, ge=1, le=100)
    ):
        """List all communities"""
        if not graphiti_instance:
            raise HTTPException(status_code=503, detail="Service not initialized")

        try:
            query = f"""
            MATCH (c:Community)
            RETURN c.name AS name, c.summary AS summary, c.size AS size
            ORDER BY c.size DESC
            LIMIT {limit}
            """

            async with graphiti_instance.driver.session() as session:
                result = await session.run(query)
                communities = await result.data()

            return {
                "total": len(communities),
                "communities": communities
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list communities: {str(e)}")

    return app


# Create app instance for uvicorn
app = create_app()

