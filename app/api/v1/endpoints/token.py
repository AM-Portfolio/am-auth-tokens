from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.core.security import create_access_token, Token
from app.services.user_validation import (
    UserValidationService, 
    UserCredentials,
    user_validation_service
)
from app.api.v1.deps import get_user_validation_service
from shared_infra.config.settings import settings


router = APIRouter()


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    username: str
    email: str


@router.post("/tokens", response_model=TokenResponse)
async def create_token(
    token_request: TokenRequest,
    user_service: UserValidationService = Depends(get_user_validation_service)
):
    """
    Create a new access token for valid user credentials.
    
    Args:
        token_request: User credentials for token creation
        user_service: User validation service dependency
    
    Returns:
        TokenResponse with access token and user information
    
    Raises:
        HTTPException: If credentials are invalid
    """
    # Validate user credentials
    credentials = UserCredentials(
        username=token_request.username,
        password=token_request.password
    )
    
    validation_result = await user_service.validate_user_credentials(credentials)
    
    if not validation_result.valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=validation_result.message or "Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create token with user data
    user_data = {
        "username": validation_result.username,
        "email": validation_result.email,
        "scopes": validation_result.scopes
    }
    
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=validation_result.user_id,
        user_data=user_data,
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.JWT_EXPIRE_MINUTES * 60,  # Convert to seconds
        user_id=validation_result.user_id,
        username=validation_result.username,
        email=validation_result.email
    )


@router.post("/tokens/oauth", response_model=TokenResponse)
async def create_token_oauth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserValidationService = Depends(get_user_validation_service)
):
    """
    OAuth2 compatible token endpoint.
    
    Args:
        form_data: OAuth2 password form data
        user_service: User validation service dependency
    
    Returns:
        TokenResponse with access token and user information
    
    Raises:
        HTTPException: If credentials are invalid
    """
    # Validate user credentials
    credentials = UserCredentials(
        username=form_data.username,
        password=form_data.password
    )
    
    validation_result = await user_service.validate_user_credentials(credentials)
    
    if not validation_result.valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=validation_result.message or "Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create token with user data
    user_data = {
        "username": validation_result.username,
        "email": validation_result.email,
        "scopes": validation_result.scopes
    }
    
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=validation_result.user_id,
        user_data=user_data,
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.JWT_EXPIRE_MINUTES * 60,  # Convert to seconds
        user_id=validation_result.user_id,
        username=validation_result.username,
        email=validation_result.email
    )