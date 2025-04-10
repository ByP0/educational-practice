import bcrypt
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
import jwt

from backend.config import secret_key, algorithm 


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid


dependencies=[Depends(JWTBearer())]

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm])
        data_now = datetime.now(timezone.utc)
        if decoded_token.get("exp") <= int(data_now.timestamp()):
            return None
        if decoded_token.get("type") != "access":
            return None
        return decoded_token
    except:
        return None

def sign_jwt(data: int) -> str:
    payload = {"sub": data}
    expire = datetime.now(timezone.utc) + timedelta(days=3)
    payload.update({"exp": expire, "type": "access"})
    return jwt.encode(payload, secret_key, algorithm=algorithm)

def sing_refresh_jwt(data: int) -> str:
    payload = {"sub": data}
    expire = datetime.now(timezone.utc) + timedelta(days=3)
    payload.update({"exp": expire, "type": "refresh"})
    return jwt.encode(payload, secret_key, algorithm=algorithm)

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)
