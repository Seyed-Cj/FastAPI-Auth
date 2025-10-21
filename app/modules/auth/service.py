from datetime import datetime
from sqlalchemy.orm import Session
from app.modules.auth import models
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from typing import Optional

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user_name: str, email: str, password: str) -> models.User:
    user = models.User(email=email, user_name=user_name, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def save_refresh_token(db: Session, user: models.User, token: str, expires_at: datetime):
    rt = models.RefreshToken(token=token, user_id=user.id, expires_at=expires_at)
    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt

def revoke_refresh_token(db: Session, token: str):
    rt = db.query(models.RefreshToken).filter(models.RefreshToken.token == token).first()
    if rt:
        rt.revoked = True
        db.commit()

def find_valid_refresh(db: Session, token: str) -> Optional[models.RefreshToken]:
    rt = db.query(models.RefreshToken).filter(models.RefreshToken.token == token, models.RefreshToken.revoked == False).first()
    if not rt:
        return None
    if rt.expires_at < datetime.utcnow():
        return None
    return rt

def rotate_refresh_token(db: Session, old_token: str, user: models.User):
    # revoke old, create new
    revoke_refresh_token(db, old_token)
    new_token, expires = create_refresh_token()
    save_refresh_token(db, user, new_token, expires)
    return new_token, expires

def create_tokens_for_user(db: Session, user: models.User):
    access_token, expire = create_access_token(subject=str(user.id))
    refresh_token, refresh_expires = create_refresh_token()
    save_refresh_token(db, user, refresh_token, refresh_expires)
    return access_token, expire, refresh_token, refresh_expires