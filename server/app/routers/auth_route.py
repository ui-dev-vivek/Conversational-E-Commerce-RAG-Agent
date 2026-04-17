from app.config.database import get_db
from app.schema.auth_schema import LoginRequest, RegisterRequest, RefreshTokenRequest, LogoutRequest
from app.services.auth_service import AuthService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

route = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)


@route.post("/register")
def register(
    request: RegisterRequest, service: AuthService = Depends(get_auth_service)
):
    registered_user = service.register(
        request.email, request.password, request.full_name
    )
    return registered_user


@route.post("/login")
def login(request: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return service.login(request.email, request.password)


@route.post("/refresh")
def refresh(request: RefreshTokenRequest, service: AuthService = Depends(get_auth_service)):
    """
    Refresh Access Token
    - Send refresh_token in body
    - Returns new access_token with same bearer type
    """
    return service.refresh_access_token(request.refresh_token)


@route.post("/logout")
def logout(request: LogoutRequest, service: AuthService = Depends(get_auth_service)):
    """
    Logout and Revoke Token
    - Send refresh_token in body
    - Marks token as revoked in database
    """
    return service.logout(request.refresh_token)
