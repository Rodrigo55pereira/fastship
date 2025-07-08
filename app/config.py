from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote

_base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore",
)


class DatabaseSettings(BaseSettings):

    # BaseSettings vai procurar esses valores dentro do arquivo .env
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: str

    # Fala pra classe aonde esta o arquivo .env
    model_config = _base_config

    @property
    def POSTGRES_URL(self):
        encoded_password = quote(self.POSTGRES_PASSWORD)  # ESCAPA a senha
        str_conn = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{encoded_password}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        return str_conn


class SecuritySettings(BaseSettings):

    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = _base_config


db_settings = DatabaseSettings()  # type: ignore
security_settings = SecuritySettings()  # type: ignore
