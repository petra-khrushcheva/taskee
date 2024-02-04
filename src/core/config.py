import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_password: str
    db_username: str
    db_echo: bool

    secret_key: str

    project_name: str
    version: str

    model_config = SettingsConfigDict(
        env_file=f"{os.path.dirname(os.path.abspath(__file__))}/../../.env"
    )

    @property
    def DATABASE_URL(self):
        return (f'postgresql+asyncpg://{self.db_username}:'
                f'{self.db_password}@{self.db_hostname}:'
                f'{self.db_port}/{self.db_name}')


settings = Settings()
