from .base import *
import environ
import os

# environ 초기화
env = environ.Env()

DEBUG = True # temp #  개발 끝나면 False로 변경 예정

# .env 파일 로드
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# .env 파일에서 도메인 목록을 읽어옴
ALLOWED_HOSTS = [h.strip() for h in env("DJANGO_ALLOWED_HOSTS").split(",")]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["MYSQL_DATABASE"],
        "USER": os.environ["MYSQL_USER"],
        "PASSWORD": os.environ["MYSQL_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
        "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", "60")),
    }
}

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


# Django 로깅: 콘솔 + 파일(7일 보관)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[{asctime}] {levelname} {name}:{lineno} | {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "file_rotating": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "django.log"),
            "when": "D",
            "interval": 1,
            "backupCount": 7,
            "encoding": "utf-8",
            "formatter": "verbose",
        },
    },
    "root": {"handlers": ["console", "file_rotating"], "level": "INFO"},
    "loggers": {
        "django": {"handlers": ["console", "file_rotating"], "level": "WARNING", "propagate": False},
        "django.request": {"handlers": ["console", "file_rotating"], "level": "ERROR", "propagate": False},
    },
}


# HTTPS를 위한 보안 설정 활성화
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF 공격 방지를 위해 신뢰할 수 있는 출처(도메인) 설정
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]
