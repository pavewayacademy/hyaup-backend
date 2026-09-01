from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_PORT: int = 8000
    APP_VERSION: str = "1.0.0"
    APP_NAME:str = "Hyaup Backend"
    APP_DESCRIPTION:str = "Hyaup Backend API"
    GOOGLE_APPLICATION_CREDENTIALS: str = "serviceAccount.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        from_attributes=True
    )

# Create a global settings instance
settings = Settings()
    