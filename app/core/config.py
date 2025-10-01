from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "DF Test API"
    version: str = "0.1.0"
    host: str = "127.0.0.1"
    port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


