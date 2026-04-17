from app.config.authentication import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_token,
)
from app.models.users_model import User, RefreshToken
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import logging
from datetime import timedelta
import datetime
logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db):
        self.db = db

    def get_user_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()

    def user_with_token(self, user):
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
        refresh_token = create_refresh_token(data={"sub": user.email, "user_id": user.id})

        # Store refresh token in DB
        try:
            refresh_token_obj = RefreshToken(
                user_id=user.id,
                token=access_token,
                refresh_token=refresh_token,
                is_revoked=False,
            )
            self.db.add(refresh_token_obj)
            self.db.commit()
        except Exception as e:
            logger.error(f"Failed to store refresh token: {str(e)}")
            self.db.rollback()

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

        except IntegrityError:
            self.db.rollback()
            logger.warning(f"Email already registered: {email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        except Exception as e:
            self.db.rollback()
            logger.error(f"User creation failed: {str(e)}")
            raise HTTPException(status_code=500, detail="User creation failed")

        return self.user_with_token(new_user)

    def login(self, email: str, password: str):
        user = self.get_user_by_email(email)

        # Always run verification to avoid timing attacks
        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Failed login attempt for email: {email}")
            raise HTTPException(
                status_code=400, detail="Email or Password are incorrect"
            )

        return self.user_with_token(user)

    def logout(self, refresh_token: str):
        """Revoke refresh token on logout"""
        try:
            token_obj = self.db.query(RefreshToken).filter(
                RefreshToken.refresh_token == refresh_token
            ).first()
            
            if not token_obj:
                raise HTTPException(status_code=400, detail="Invalid token")
            
            token_obj.is_revoked = True
            self.db.commit()
            logger.info(f"Token revoked for user_id: {token_obj.user_id}")
            return {"message": "Logged out successfully"}
        except Exception as e:
            self.db.rollback()
            logger.error(f"Logout failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Logout failed")

    def refresh_access_token(self, refresh_token: str):
        """Generate new access token using refresh token"""
        payload = verify_token(refresh_token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Not a refresh token")
        
        # Check if token is revoked
        token_obj = self.db.query(RefreshToken).filter(
            RefreshToken.refresh_token == refresh_token
        ).first()
        
        if not token_obj or token_obj.is_revoked:
            raise HTTPException(status_code=401, detail="Token has been revoked")
        
        user = self.db.query(User).filter(User.id == token_obj.user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Create new access token
        new_access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )
        
        logger.info(f"Access token refreshed for user_id: {user.id}")
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
