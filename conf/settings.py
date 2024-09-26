import os

IS_PROD = bool(int(os.getenv('IS_BASE_USER_PROD', '0')))

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 43200

IS_SECURE_COOKIE = IS_PROD
SAME_SITE = 'lax'

APP_NAME = os.getenv('APP_NAME', 'BaseUsers')

JAEGER_BACKEND = os.getenv('JAEGER_BACKEND', 'localhost:4317')

GMAIL_API_TOKEN = os.getenv('GMAIL_API_TOKEN', '')
FRONTEND_URL = os.getenv('BASE_USERS_FRONTEND_URL', 'http://testing.internal:3000')

ALLOWED_ORIGINS = [FRONTEND_URL] if IS_PROD else ['http://localhost:3000', 'http://testing.internal', FRONTEND_URL]

S3_ENDPOINT = os.getenv('BASE_USERS_S3_ENDPOINT', '')
BUCKET = os.getenv('BASE_USERS_BUCKET', '')
IS_S3_MOCK = os.getenv('IS_S3_MOCK', '0')
