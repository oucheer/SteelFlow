from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str
    jwt_secret: str
    webhook_secret: str
    seed_password: str
    frontend_origin: str = "http://127.0.0.1:5173"


settings = Settings()
