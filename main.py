from fastapi import Response
from fastapi import Depends
from fastapi import Header
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from models.user_credentials import UserCredentials

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Auth API with Supabase")

def check_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Access token required"}
        )
    token = authorization.split(" ")[1]
    try:
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        if not user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid or expired token"}
            )
        return {"user": user, "token": token}
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"error": "Invalid or expired token"})


@app.get("/")
def root():
    return JSONResponse({"message": "Welcome to the Auth API with Supabase"})
    
    
@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: UserCredentials):
    try:
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return response
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})

@app.post("/auth/login", status_code=status.HTTP_200_OK)
def login(credentials: UserCredentials):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return response
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": str(e)})



@app.get("/public/info")
def public_info():
    return JSONResponse({"message": "Welcome stranger! This info is public."})

@app.get("/protected/profile")
def protected_profile(auth: dict = Depends(check_token)):
    return {
            "message": "Access granted!",
            "user": {
                "id": auth['user'].id,
                "email": auth['user'].email,
                "created_at": str(auth['user'].created_at)
            }
        }

@app.post("/auth/logout",status_code=status.HTTP_200_OK,dependencies=[Depends(check_token)])
def logout():
    try:
        supabase.auth.sign_out()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )