import json
import os
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status as http_status_code
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from app.api.security.common import SECRET_KEY, ALGORITHM
from app.api.security.hash import verify_password
from app.core.postgres.queries.user import get_by_username
from app.core.postgres.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=http_status_code.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_by_username(username)
    if user is None:
        raise credentials_exception
    return user


def roles_required(*required_roles: str):
    def role_dependency(current_user: User = Depends(get_current_user)):
        user_roles = {role.name for role in current_user.roles}
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=http_status_code.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_dependency


async def authenticate_user(username: str, password: str):
    user: Optional[User] = await get_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user