from pydantic_settings import BaseSettings, SettingsConfigDict

env_state = ".prod"

class Settings(BaseSettings):
    custom_epoch: int
    database_url: str
    client_url: str
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    model_config = SettingsConfigDict(env_file=f"../.env{env_state}")

# Immediately instantiate settings obj
settings = Settings()