from fastapi import FastAPI, HTTPException, status
from typing import Dict
from pydantic import BaseModel

# Initialize FastAPI app with metadata
app = FastAPI(
    title="My FastAPI Application",
    description="A enhanced Hello World API with best practices",
    version="1.0.0"
)

# Health check endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict:
    return {"status": "healthy"}

# Main endpoint with enhanced response
@app.get("/", status_code=status.HTTP_200_OK)
async def root() -> Dict:
    return {
        "message": "Hello World",
        "status": "success",
        "version": "1.0.0"
    }

# Error handling example
@app.get("/error-example")
async def error_example():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="This is an example error response"
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    print("Application is starting up...")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")