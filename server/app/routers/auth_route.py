from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schema.auth_schema import LoginRequest, RegisterRequest
from app.config.database import get_db
from app.services.auth_service import AuthService

route = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)


@route.post("/register")
def register(
    request: RegisterRequest,
    service: AuthService = Depends(get_auth_service)
):
    if(service.get_user_by_email(request.email)):
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    registered_user = service.register(
        request.email,
        request.password,
        request.full_name
    )
    return registered_user


@route.post("/login")
def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    return service.login(
        request.username,
        request.password
    )