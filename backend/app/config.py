from pydantic import BaseSettings

class Settings(BaseSettings):
    PORT_ : str = "80"
    IP_: str

    class Config:
        env_file = ".env"