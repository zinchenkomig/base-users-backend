import hashlib
import hmac
from copy import copy
from datetime import datetime, timedelta
from typing import Union
from jose import jwt
from passlib.context import CryptContext
from conf.secrets import PASSWORD_ENCODING_SECRET
from conf import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, PASSWORD_ENCODING_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_data_string(data: dict):
    sorted_data = sorted(data.items(), key=lambda x: x[0])
    sorted_data_str = '\n'.join([f'{key}={val}' for key, val in sorted_data])
    return sorted_data_str


def is_tg_hash_valid(data: dict, tg_bot_token: str):
    d = copy(data)
    data_hash = d.pop('hash')
    data_str = get_data_string(d)
    secret_hashed = hashlib.sha256(tg_bot_token.encode())
    one = hmac.new(key=secret_hashed.digest(), msg=data_str.encode(), digestmod='sha256')
    return hmac.compare_digest(one.hexdigest(), data_hash)
