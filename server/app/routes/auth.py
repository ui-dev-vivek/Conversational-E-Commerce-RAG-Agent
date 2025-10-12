from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/login")
async def login(username: str, password: str):
    # Placeholder: integrate real auth (JWT/session)
    if username == "admin" and password == "password":
        return {"access_token": "fake-token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/register")
async def register(username: str, password: str):
    # Placeholder: create user
    return {"username": username, "status": "created"}
