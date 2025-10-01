#!/usr/bin/env python3
"""
Simple mock user management service for development testing.
Run this on port 8001 to simulate the am-user-management service.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Mock User Management Service", version="1.0.0")


class CredentialsRequest(BaseModel):
    username: str
    password: str


@app.post("/internal/validate-credentials")
async def validate_credentials(credentials: CredentialsRequest):
    """Mock endpoint that accepts any credentials."""
    # In a real service, you'd validate against a database
    # For testing, we'll accept any credentials
    return {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "username": credentials.username,
        "email": f"{credentials.username}@example.com",
        "scopes": ["read", "write", "admin"]
    }


@app.get("/internal/users/{user_id}")
async def get_user(user_id: str):
    """Mock endpoint to get user by ID."""
    return {
        "user_id": user_id,
        "username": "testuser",
        "email": "testuser@example.com",
        "scopes": ["read", "write", "admin"],
        "active": True
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "mock-user-management"
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Mock User Management Service",
        "status": "running",
        "endpoints": [
            "POST /internal/validate-credentials",
            "GET /internal/users/{user_id}",
            "GET /health"
        ]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)