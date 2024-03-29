import pathlib

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_password: str
    db_username: str
    db_echo: bool

    secret_key: SecretStr

    project_name: str
    project_version: str
    jwt_lifetime_seconds: int

    model_config = SettingsConfigDict(
        env_file=f"{pathlib.Path(__file__).parents[2]}/.env",
        extra="ignore",
    )

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.db_username}:"
            f"{self.db_password}@{self.db_hostname}:"
            f"{self.db_port}/{self.db_name}"
        )


settings = Settings()
