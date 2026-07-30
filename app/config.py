from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    worker_id: int
    custom_epoch: int

    model_config = SettingsConfigDict(env_file=".env")

# Immediately instantiate settings obj
settings = Settings()