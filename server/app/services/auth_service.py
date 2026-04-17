from fastapi import HTTPException
from app.models.users_model import User
from app.config.authentication import hash_password, create_access_token


class AuthService:
    def __init__(self, db):
        self.db = db

    def get_user_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()

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
                is_active=True
            )

            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="User creation failed")

        # create token
        access_token = create_access_token(
            data={"sub": new_user.email, "user_id": new_user.id}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "full_name": new_user.full_name
            }
        }