# settings.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Varnamala"
    debug: bool = True
    host: str
    port: int

    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    cirus_db_host: str | None = None
    cirus_db_port: int | None = None
    cirus_db_user: str | None = None
    cirus_db_password: str | None = None
    cirus_db_name: str | None = None

    class Config:
        env_file = ".env"
        # from_attributes = True

    @property
    def db_url(self):
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

@lru_cache()
def get_settings():
    return Settings()
