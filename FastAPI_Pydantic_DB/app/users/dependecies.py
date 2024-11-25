from jose import jwt, JWTError, ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from fastapi import Request, HTTPException, status, Depends
from app.config import settings
from datetime import datetime, timezone
from app.users.services_dao import UsersDAO


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
        raise credentials_exception("Token has expired")
    except JWTError:
        raise credentials_exception("Invalid Token")

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise credentials_exception("Token has expired..")

    user_id: str = payload.get("sub")
    if not user_id:
        raise credentials_exception("Used ID hasn't found")

    username = await UsersDAO.find_by_id(int(user_id))
    if not username:
        raise credentials_exception("User hasn't found")

    return username
