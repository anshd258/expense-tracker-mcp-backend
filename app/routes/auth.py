from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import create_access_token
from app.core.config import settings
from app.core.auth import get_current_user
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.models.user import user_service
from app.utils.exceptions import ConflictException, UnauthorizedException

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, summary="Register new user")
async def register(user_data: UserCreate):
    """Register a new user account"""
    # Check if user already exists
    existing_user = await user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise ConflictException("Email already registered")
    
    # Create new user
    created_user = await user_service.create_user(user_data)
    return UserResponse(**created_user)


@router.post("/login", response_model=Token, summary="User login (Form)")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return access token (for OAuth2 form compatibility)"""
    # Authenticate user
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException("Incorrect email or password")
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/token", response_model=Token, summary="User login (JSON)")
async def login_json(user_credentials: UserLogin):
    """Authenticate user and return access token (JSON payload)"""
    # Authenticate user
    user = await user_service.authenticate_user(user_credentials.email, user_credentials.password)
    if not user:
        raise UnauthorizedException("Incorrect email or password")
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse, summary="Get current user")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user information"""
    return UserResponse(**current_user)