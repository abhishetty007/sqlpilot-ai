from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.auth import login, init_users_table

app = FastAPI(
    title="NL→SQL AI API",
    version="1.0.0"
)

# Create users table when server starts
init_users_table()


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def home():
    return {
        "message": "Welcome to NL→SQL AI Backend 🚀"
    }


@app.post("/login")
def login_user(data: LoginRequest):

    ok, user_id = login(
        data.username,
        data.password
    )

    if not ok:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "success": True,
        "user_id": user_id,
        "username": data.username
    }