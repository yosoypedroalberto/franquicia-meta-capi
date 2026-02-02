from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    PROJECT_NAME: str = "Meta Franchise"
    MONGODB_URL: str
    FB_ACCESS_TOKEN: str
    TELEGRAM_BOT_TOKEN: str
    class Config:
        env_file = ".env"
settings = Settings()
