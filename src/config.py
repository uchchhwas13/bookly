from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    JWT_ACCESS_TOKEN_SECRET_KEY: str = ""
    JWT_REFRESH_TOKEN_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = ""
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


config = Settings()
