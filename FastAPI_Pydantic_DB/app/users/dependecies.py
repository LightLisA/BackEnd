from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Request, Depends
from app.config import settings
from datetime import datetime, timezone
from app.users.models import Users
from app.users.services_dao import UsersDAO
from app.exeptions import *


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


async def get_current_user(jwt_token: str = Depends(get_token)):
    credentials_exception = lambda detail: HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            jwt_token,
            settings.SECRET_KEY,
            settings.ALGORITHM
        )
    except ExpiredSignatureError:
        raise HTTPException_InvalidToken
    except JWTError:
        raise HTTPException_IncorrectTokenFormat

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException_TokenExpired

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException_UserIdNotFound

    username = await UsersDAO.find_by_id(int(user_id))
    if not username:
        raise HTTPException_UserNotFound

    return username


async def get_admin_users(current_user: Users = Depends(get_current_user)):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=401)
    return current_user
