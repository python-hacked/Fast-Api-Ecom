from pydantic import BaseSettings


class Setting(BaseSettings):
    db_connection: str
    db_host: str
    db_port: str
    db_database: str
    db_username: str
    db_password: str
   

    class Config:
        env_file = ".env"
