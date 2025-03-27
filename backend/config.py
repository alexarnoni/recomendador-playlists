from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    ADMIN_TOKEN: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
