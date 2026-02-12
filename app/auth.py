from fastapi import APIRouter, HTTPException
from app.models import LoginRequest, TokenResponse, User
import re

router = APIRouter(prefix="/auth", tags=["authentication"])

# Mock database
users_db = {
    "user@example.com": {
        "password": "hashed_password123",
        "username": "testuser",
        "full_name": "Test User"
    }
}

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """
    Login endpoint that validates credentials and returns JWT token.
    
    Args:
        request: LoginRequest with email and password
        
    Returns:
        TokenResponse with access token
        
    Raises:
        HTTPException: If email is invalid or credentials are wrong
    """
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, request.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Validate password is not empty
    if not request.password or len(request.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    user = users_db.get(request.email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # In production, generate a real JWT token
    token = f"token_{request.email}"
    
    return TokenResponse(access_token=token, token_type="bearer")

@router.get("/me", response_model=User)
def get_current_user():
    """
    Get current authenticated user information.
    """
    return User(
        id=1,
        username="testuser",
        email="user@example.com",
        full_name="Test User",
        is_active=True
    )
