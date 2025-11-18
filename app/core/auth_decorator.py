from functools import wraps
from fastapi import Request, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timezone
from typing import Optional
SECRET_KEY = "VARNAMALA_SECRET_KEY"
ALGORITHM = "HS256"

def token_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Find `Request` in args (FastAPI passes it automatically if we add it in route signature)
        request: Optional[Request] = next(
            (arg for arg in args if isinstance(arg, Request)),
            kwargs.get("request")
        )

        if not request:
            raise RuntimeError("Request object not found in route")

        # Extract header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp = payload.get("exp")
            current_time = datetime.now(timezone.utc).timestamp()
            
            if exp and current_time > exp:
                raise HTTPException(status_code=401, detail="Token expired")

            # Attach user info into request.state
            request.state.user = payload.get("sub")

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await func(*args, **kwargs)
    return wrapper
