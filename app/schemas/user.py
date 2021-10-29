from pydantic import BaseModel


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


class UserDB(UserBase):
    class Config:
        orm_mode = True


class UserOut(UserDB):
    id: int


class UserInDB(UserDB):
    hashed_password: str
