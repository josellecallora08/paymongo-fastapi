from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password:str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True