# app/utils/password.py
from passlib.context import CryptContext
import logging


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hashed_password: str) -> bool:
    logging.debug("verify_password called")
    result = pwd_context.verify(
        secret=password,
        hash=hashed_password
    )
    logging.debug(f"verify_password result={result}")
    return result

def hash_password(password: str) -> str:
    logging.debug("hash_password called")
    return pwd_context.hash(
        secret=password
    )