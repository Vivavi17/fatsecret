import redis.asyncio as redis
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_PORT: int
    DB_HOST: str
    DB_USER: str
    DB_PASS: str

    secret: str
    algorithm: str

    REDIS_PORT: int
    REDIS_HOST: str

    token_life: int

    BOT_TOKEN: str

    @property
    def URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
