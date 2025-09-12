from jose import JWTError, jwt

from app.api.security.common import SECRET_KEY, ALGORITHM


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


