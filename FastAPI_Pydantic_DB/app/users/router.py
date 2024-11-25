from fastapi import APIRouter, HTTPException, status, Response
from app.users.schemas import SUserAuth
from app.users.services_dao import UsersDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from datetime import timedelta


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"]
)


@router.post("/register")
async def register_user(user_date: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_date.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_date.password)
    await UsersDAO.add(email=user_date.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_date: SUserAuth):
    user = await authenticate_user(user_date.email, user_date.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": user[0].id}, expires_delta=timedelta(minutes=30))
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token
