from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY:str = "secretkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PAYMONGO_PUBLIC_KEY: str 
    PAYMONGO_SECRET_KEY: str
    PAYMONGO_TOKEN: str

    class Config:
        env_file = '.env'

settings = Settings()