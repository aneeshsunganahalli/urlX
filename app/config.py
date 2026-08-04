from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    worker_id: int
    custom_epoch: int
    database_url: str
    client_url: str
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    model_config = SettingsConfigDict(env_file=".env")

# Immediately instantiate settings obj
settings = Settings()