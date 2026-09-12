from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Fortune-telling Cards API"
    database_url: str = "sqlite:///./Database/fortune_cards.db"
    default_lang: str = "uk"  # uk | ru | en

    class Config:
        env_file = ".env"


settings = Settings()
