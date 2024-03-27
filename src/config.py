from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    MODE: str
    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file=".env")


config = Config()