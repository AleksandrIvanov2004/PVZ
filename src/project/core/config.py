from pydantic_settings import BaseSettings
from pydantic import SecretStr
class Settings(BaseSettings):
    # TODO убрать значения по умолчанию при переносе приложения в Docker
    ORIGINS: str = "*"
    ROOT_PATH: str = ""
    ENV: str = "DEV"
    LOG_LEVEL: str = "DEBUG"
    POSTGRES_SCHEMA: str = "public"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "pvz"
    POSTGRES_PORT: int = 5437
    POSTGRES_USER: SecretStr = "postgres"
    POSTGRES_PASSWORD: SecretStr = "postgres"
    POSTGRES_RECONNECT_INTERVAL_SEC: int = 1

    JWT_SECRET_KEY: SecretStr
    HASH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def postgres_url(self) -> str:
        creds = f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
settings = Settings()
