import logging
import uuid
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from passlib.context import CryptContext

from src.config import Config

ACCESS_TOKEN_EXPIRY = 3600
password_context = CryptContext(schemes=["argon2"], deprecated="auto")
serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, salt="email-configuration"
)


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password_hash(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
) -> str:
    payload = {
        "user": user_data,
        "exp": datetime.now()
        + (expiry if expiry is not None else timedelta(minutes=60)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str):
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


def create_url_safe_token(data: dict, expiration=3600):
    return serializer.dumps(data)


def decode_url_safe_token(token: str, max_age=3600):
    try:
        # Deserialize the token and check if it's expired
        data = serializer.loads(token, max_age=max_age)
        return data
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")
