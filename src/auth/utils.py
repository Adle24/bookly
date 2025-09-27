from passlib.context import CryptContext

password_context = CryptContext(schemes=["argon2"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password_hash(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)
