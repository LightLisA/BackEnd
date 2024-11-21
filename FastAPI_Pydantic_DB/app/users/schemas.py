from datetime import date
from pydantic import BaseModel, EmailStr


class SUserRegister(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
