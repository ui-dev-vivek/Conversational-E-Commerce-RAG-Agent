from app.config.authentication import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.users_model import User
from fastapi import HTTPException


class AuthService:
    def __init__(self, db):
        self.db = db

    def get_user_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()

    def user_with_token(self, user):
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
        refresh_token = create_refresh_token(
            data={"sub": user.email, "user_id": user.id}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
            },
        }

    def register(self, email, password, full_name):
        # check duplicate
        existing_user = self.get_user_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        try:
            hashed_password = hash_password(password)

            new_user = User(
                email=email,
                username=email,
                hashed_password=hashed_password,
                full_name=full_name,
                is_active=True,
            )

            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="User creation failed")

        return self.user_with_token(user)

    def login(self, email: str, password: str):
        user = self.get_user_by_email(email)

        # Always run verification to avoid timing attacks
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=400, detail="Email or Password are incorrect"
            )

        return self.user_with_token(user)
