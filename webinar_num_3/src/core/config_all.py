import os
from pathlib import Path
from datetime import timedelta

VERSION: str = "1.0.0"

# JWT SETTINGS
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "foo")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_EXPIRES_S: int = os.getenv("JWT_ACCESS_EXPIRES_S", timedelta(minutes=10))
JWT_REFRESH_EXPIRES_S: int = os.getenv("JWT_REFRESH_EXPIRES_S", timedelta(days=15))

# Название проекта. Используется в Swagger-документации
PROJECT_NAME: str = os.getenv("PROJECT_NAME", "webinar_num_3")

# Настройки Redis
REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
CACHE_EXPIRE_IN_SECONDS: int = 60 * 5  # 5 минут

# Настройки Postgres
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "webinar_num_3")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "webinar_num_3")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "webinar_num_3")

DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent