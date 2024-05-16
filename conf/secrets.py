import os
from . import settings

db_address = os.getenv('BASE_USERS_DB_ADDRESS')
db_user = os.getenv('BASE_USERS_DB_USER')
db_password = os.getenv('BASE_USERS_DB_PASSWORD')
db_name = os.getenv('BASE_USERS_DB_NAME')

tg_secret_token = os.getenv('BASE_USERS_TG_TOKEN')

PASSWORD_ENCODING_SECRET = os.environ['BASE_USERS_PASS_ENCODING_SECRET']
# to get a string like this run:
# openssl rand -hex 32


if settings.IS_PROD and None in (db_address, db_name, db_user, db_password):
    raise ValueError("Database connection env is not set")
