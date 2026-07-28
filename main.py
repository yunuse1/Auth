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
def protected_profile(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Access token required"}
        )
    return {
        "message": "Token received, but not verified yet!",
        "raw_token": authorization.split(" ")[1]
    }