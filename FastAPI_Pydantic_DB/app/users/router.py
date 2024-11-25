from fastapi import APIRouter, Response, Depends
from app.users.schemas import SUserAuth
from app.users.services_dao import UsersDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from datetime import timedelta
from app.users.dependecies import get_current_user, get_admin_users
from app.users.models import Users
from app.exeptions import *


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"]
)


@router.post("/register")
async def register_user(user_date: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_date.email)
    if existing_user:
        raise HTTPException_UserAlreadyExists
    hashed_password = get_password_hash(user_date.password)
    await UsersDAO.add(email=user_date.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_date: SUserAuth):
    user = await authenticate_user(user_date.email, user_date.password)
    if not user:
        raise HTTPException_IncorrectEmailOrPassword
    access_token = create_access_token({"sub": str(user[0].id)}, expires_delta=timedelta(minutes=30))
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    msg = "Used has been logout"
    return msg


@router.get("/me")
async def get_users_me_info(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def get_users_all_info(current_user: Users = Depends(get_admin_users)):
    return await UsersDAO.find_all()
