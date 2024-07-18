from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEBUG: bool
    LOG_LEVEL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
