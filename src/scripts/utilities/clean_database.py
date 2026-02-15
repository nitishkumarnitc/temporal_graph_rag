"""Clean Neo4j database - remove all nodes, relationships, and indices"""
import asyncio
import os
from graphiti_core import Graphiti
from dotenv import load_dotenv

load_dotenv()


async def clean_database():
    """Clean all data from Neo4j database"""
    print("=" * 80)
    print("CLEANING NEO4J DATABASE")
    print("=" * 80)

    from neo4j import AsyncGraphDatabase

    driver = AsyncGraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://neo4j:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "graph_rag"))
    )
    
    async with driver.session() as session:
        # Delete all nodes and relationships
        print("🗑️  Deleting all nodes and relationships...")
        result = await session.run("MATCH (n) DETACH DELETE n")
        await result.consume()
        print("✅ All nodes and relationships deleted")
        
        # Drop all indices
        print("\n🗑️  Dropping all indices...")
        result = await session.run("SHOW INDEXES")
        indices = await result.data()
        
        for index in indices:
            index_name = index.get('name')
            if index_name:
                try:
                    await session.run(f"DROP INDEX {index_name} IF EXISTS")
                    print(f"   ✅ Dropped index: {index_name}")
                except Exception as e:
                    print(f"   ⚠️  Could not drop index {index_name}: {e}")
        
        # Drop all constraints
        print("\n🗑️  Dropping all constraints...")
        result = await session.run("SHOW CONSTRAINTS")
        constraints = await result.data()
        
        for constraint in constraints:
            constraint_name = constraint.get('name')
            if constraint_name:
                try:
                    await session.run(f"DROP CONSTRAINT {constraint_name} IF EXISTS")
                    print(f"   ✅ Dropped constraint: {constraint_name}")
                except Exception as e:
                    print(f"   ⚠️  Could not drop constraint {constraint_name}: {e}")
        
        # Verify database is empty
        print("\n📊 Verifying database is clean...")
        result = await session.run("MATCH (n) RETURN count(n) as count")
        record = await result.single()
        node_count = record['count']
        
        result = await session.run("MATCH ()-[r]->() RETURN count(r) as count")
        record = await result.single()
        rel_count = record['count']
        
        print(f"   Nodes: {node_count}")
        print(f"   Relationships: {rel_count}")
    
    await driver.close()
    
    print("\n" + "=" * 80)
    print("✅ DATABASE CLEANED SUCCESSFULLY!")
    print("=" * 80)
    print()


if __name__ == "__main__":
    asyncio.run(clean_database())

