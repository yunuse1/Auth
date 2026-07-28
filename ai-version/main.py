import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Response,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from supabase import Client, create_client

# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="FastAPI + Supabase Auth API",
    version="1.0.0",
)

# Adds the padlock button in Swagger UI.
security = HTTPBearer()


# --------------------------------------------------------------------
# Request Models
# --------------------------------------------------------------------

class AuthRequest(BaseModel):
    email: str
    password: str


# --------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------

def validate_auth_input(email: str, password: str):
    if not email.strip() or not password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password cannot be empty.",
        )


def get_access_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
):
    """
    Extracts the Bearer token from the Authorization header.
    """

    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"},
        )

    return credentials.credentials


def get_current_user(token: str = Depends(get_access_token)):
    """
    Verifies the JWT access token using Supabase.
    """

    try:
        user_response = supabase.auth.get_user(token)

        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid or expired token"},
            )

        return user_response.user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid or expired token"},
        )


# --------------------------------------------------------------------
# Auth Endpoints
# --------------------------------------------------------------------

@app.post(
    "/auth/signup",
    status_code=status.HTTP_201_CREATED,
)
def signup(payload: AuthRequest):
    validate_auth_input(payload.email, payload.password)

    try:
        result = supabase.auth.sign_up(
            {
                "email": payload.email,
                "password": payload.password,
            }
        )

        return {
            "message": "User registered successfully.",
            "user_id": result.user.id if result.user else None,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@app.post("/auth/login")
def login(payload: AuthRequest):
    validate_auth_input(payload.email, payload.password)

    try:
        result = supabase.auth.sign_in_with_password(
            {
                "email": payload.email,
                "password": payload.password,
            }
        )

        if result.session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials.",
            )

        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )


@app.post(
    "/auth/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    token: str = Depends(get_access_token),
):
    """
    Protected endpoint.
    Requires a valid access token.
    """

    try:
        # Verify token first.
        supabase.auth.get_user(token)

        # Sign out the currently authenticated session.
        supabase.auth.sign_out()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid or expired token"},
        )


# --------------------------------------------------------------------
# Public Endpoint
# --------------------------------------------------------------------

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome to the public API endpoint."
    }


# --------------------------------------------------------------------
# Protected Endpoint
# --------------------------------------------------------------------

@app.get("/protected/profile")
def profile(user=Depends(get_current_user)):
    return {
        "user_id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }