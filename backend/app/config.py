from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Set DATABASE_URL to use SQLite (dev) or leave unset to use MSSQL settings below
    database_url: Optional[str] = None
    db_server: Optional[str] = None
    db_name: Optional[str] = None
    db_username: Optional[str] = None
    db_password: Optional[str] = None
    db_driver: str = "ODBC Driver 17 for SQL Server"
    secret_key: str = "dev-secret-key-change-before-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        driver = quote_plus(self.db_driver)
        password = quote_plus(self.db_password or "")
        return (
            f"mssql+pyodbc://{self.db_username}:{password}"
            f"@{self.db_server}/{self.db_name}"
            f"?driver={driver}"
        )


settings = Settings()
