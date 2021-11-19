from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str
    name: str
    career: str
    team: str
    profile_photo_path: str


class UserLogIn(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    career: Optional[str] = None
    team: Optional[str] = None
    profile_photo_path: Optional[str] = None


class UserDB(UserBase):
    class Config:
        orm_mode = True


class UserOut(UserDB):
    id: int


class UserInDB(UserDB):
    hashed_password: str
