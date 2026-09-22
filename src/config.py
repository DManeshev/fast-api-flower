from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str = ''
    DB_PORT: int = 5432
    DB_NAME: str = ''
    DB_USER: str = ''
    DB_PASSWORD: str = ''

    YANDEX_ACCESS_KEY: str = ''
    YANDEX_SECRET_KEY: str = ''

    @property
    def DATABASE_URL(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
