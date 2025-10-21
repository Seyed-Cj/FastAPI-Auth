from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    user_name: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    user_name: str
    is_active: bool
    role: str
    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: Optional[str] = None