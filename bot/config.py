from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):

    bot_token: str

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
