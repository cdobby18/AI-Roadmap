import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

# Simple in-memory user store for learning purposes.
users_db = {
    "stanleyjobson": "swordfish",
    "alice": "wonderland",
    "bob": "builder",
}


def verify_password(plain_password: str, stored_password: str) -> bool:
    return secrets.compare_digest(
        plain_password.encode("utf8"), stored_password.encode("utf8")
    )


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    username = credentials.username
    password = credentials.password

    if username not in users_db or not verify_password(password, users_db[username]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": 'Basic realm="Secure Area"'},
        )
    return username


@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}


@app.get("/secure-data")
def read_secure_data(username: Annotated[str, Depends(get_current_username)]):
    return {
        "message": f"Hello {username}, this is a protected endpoint.",
        "notes": "Use Basic Auth with correct username and password.",
    }


@app.get("/login")
def login(username: Annotated[str, Depends(get_current_username)]):
    return {
        "message": f"Login successful for {username}.",
        "help": "Then call /users/me or /secure-data with the same credentials.",
    }


@app.get("/raw-credentials")
def read_raw_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "username": credentials.username,
        "password": "hidden",
        "auth_type": "basic",
        "info": "This endpoint shows how FastAPI passes credentials. Do not expose raw passwords in production.",
    }
