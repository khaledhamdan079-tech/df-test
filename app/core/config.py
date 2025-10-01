from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "DF Test API"
    version: str = "0.1.0"
    host: str = "127.0.0.1"
    port: int = 8000
    
    # Dialogflow CX Configuration
    dialogflow_project_id: str = ""
    dialogflow_location: str = "global"
    dialogflow_agent_id: str = ""
    google_application_credentials: str = ""  # Path to your JSON key file

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


