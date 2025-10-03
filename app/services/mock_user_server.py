#!/usr/bin/env python3
"""
Simple mock user management service for development testing.
Run this on port 8001 to simulate the am-user-management service.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import time

app = FastAPI(title="Mock User Management Service", version="1.0.0")


class CredentialsRequest(BaseModel):
    username: str
    password: str


@app.post("/api/v1/auth/login")
async def login(credentials: CredentialsRequest):
    """Mock login endpoint that mimics am-user-management."""
    # In a real service, you'd validate against a database
    # For testing, we'll accept any credentials
    return {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "email": credentials.username,  # username is expected to be email
        "status": "active",
        "session_id": f"session_{credentials.username}_{int(time.time())}",
        "last_login_at": "2025-10-01T12:00:00.000000+00:00",
        "requires_verification": False
    }


@app.post("/internal/validate-credentials")
async def validate_credentials(credentials: CredentialsRequest):
    """Legacy endpoint for backward compatibility."""
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