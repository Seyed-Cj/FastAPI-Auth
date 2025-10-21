# app/modules/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from app.modules.auth import schemas, service
from app.shared.deps import get_db_dep, get_current_user
from app.core.db import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if service.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = service.create_user(db, payload.user_name, payload.email, payload.password)
    return user

@router.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token, access_expires, refresh_token, refresh_expires = service.create_tokens_for_user(db, user)
    expires_in = int((access_expires - datetime.utcnow()).total_seconds())
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "expires_in": expires_in
    }

@router.post("/token/refresh", response_model=schemas.TokenResponse)
def refresh_token(refresh_token: str = Body(...), db: Session = Depends(get_db)):
    rt = service.find_valid_refresh(db, refresh_token)
    if not rt:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user = service.get_user(db, rt.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # rotate refresh token
    new_refresh, new_refresh_expires = service.rotate_refresh_token(db, refresh_token, user)
    access_token, access_expires, _, _ = service.create_tokens_for_user(db, user)
    expires_in = int((access_expires - datetime.utcnow()).total_seconds())
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh,
        "expires_in": expires_in
    }

@router.post("/logout")
def logout(refresh_token: str = Body(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # revoke provided refresh token
    service.revoke_refresh_token(db, refresh_token)
    return {"msg": "logged out"}

@router.get("/me", response_model=schemas.UserOut)
def me(current_user = Depends(get_current_user)):
    return current_user