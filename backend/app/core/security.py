from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta, timezone

from app.config import secret_key, algorithm, expire_minutes, expire_days


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
 
    def verify_jwt(self, jwt_token: str):
        isTokenValid: bool = False

        try:
            payload = decode_access_jwt(jwt_token)
        except:
            payload = None
        if payload:
            isTokenValid = True
        
        return isTokenValid
    

dependencies=[Depends(JWTBearer())]

def generate_access_jwt(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(expire_minutes))
    payload.update({"exp": expire, "type": "access"})
    return jwt.encode(payload=payload, key=secret_key, algorithm=algorithm)

def generate_refresh_jwt(data: dict) -> str:
    payload = {
        "sub": data.get("sub"),
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=int(expire_days)),
    }
    return jwt.encode(payload=payload, key=secret_key, algorithm=algorithm)

def decode_access_jwt(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, key=secret_key, algorithms=[algorithm])
        data_now = datetime.now(timezone.utc)
        if decoded_token.get("exp") <= int(data_now.timestamp()):
            return None
        if decoded_token.get("type") != "access":
            return None
        return decoded_token
    except:
        return None
    
def decode_refresh_jwt(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, key=secret_key, algorithms=[algorithm])
        data_now = datetime.now(timezone.utc)
        if decoded_token.get("exp") <= int(data_now.timestamp()):
            return None
        if decoded_token.get("type") != "refresh":
            return None
        return decoded_token
    except:
        return None
    
def set_token_pair(data: dict) -> dict[str, str]:
    return {
        "access_token": generate_access_jwt(data=data),
        "refresh_token": generate_refresh_jwt(data=data)
    }

def get_token_data(request: Request) -> dict:
    headers = request.headers
    token_list = headers.get("authorization").split()
    return decode_access_jwt(token_list[1])