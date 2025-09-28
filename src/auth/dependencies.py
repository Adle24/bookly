from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from src.auth.utils import decode_token


class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )

        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None
