from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://myuser:mypassword@postgres:5432/mydb"
    REDIS_URL: str = "redis://redis:6379/0"
    APP_NAME: str = "NeoWayCase API"

    model_config = {
        "env_file": ".env",
    }

settings = Settings()