from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Fortune-telling Cards API"
    database_url: str = "sqlite:///./database/fortune_cards.db"
    default_lang: str = "ru"  # ru | uk | en

    class Config:
        env_file = ".env"


settings = Settings()
