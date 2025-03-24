from pydantic import BaseSettings

class Settings(BaseSettings):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()
