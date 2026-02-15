"""
FastAPI REST API for Temporal Knowledge Graph RAG
DEPRECATED: Use app.py instead
This file is kept for backward compatibility with Docker
"""
from api.routes import create_app

# Create app using new modular structure
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

