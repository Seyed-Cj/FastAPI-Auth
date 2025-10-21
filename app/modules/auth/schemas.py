from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    user_name: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8, max_length=72)  

class UserOut(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    class Config:
        from_attributes = True  

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int