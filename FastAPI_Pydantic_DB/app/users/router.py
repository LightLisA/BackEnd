from fastapi import APIRouter, HTTPException
from app.users.schemas import SUserRegister
from app.users.services_dao import UsersDAO
from app.users.auth import get_password_hash


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"]
)


@router.post("/register")
async def register_user(user_date: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_date.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_date.password)
    await UsersDAO.add(email=user_date.email, hashed_password=hashed_password)
