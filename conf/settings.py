import os

IS_PROD = bool(int(os.getenv('IS_BASE_USER_PROD', '0')))

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

IS_SECURE_COOKIE = IS_PROD
SAME_SITE = 'lax'

APP_NAME = os.getenv('APP_NAME', 'BaseUsers')

JAEGER_BACKEND = os.getenv('JAEGER_BACKEND', 'localhost:4317')

GMAIL_API_TOKEN = os.getenv('GMAIL_API_TOKEN', '')
FRONTEND_URL = os.getenv('BASE_USERS_FRONTEND_URL', 'http://testing.internal:3000')

ALLOWED_ORIGINS = [FRONTEND_URL] if IS_PROD else ['http://localhost:3000', 'http://testing.internal', FRONTEND_URL]
