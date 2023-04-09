from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/autenticacao"
    DBBaseModel = declarative_base()

    JWT_SECRET: str = '82EJ682EQiEGTW533ziZbyAu0P0WbVP-NISM1X7b3vc'
    """"
    import secrets
    token str = secrets.token_urlsafe(32)
    """
    
    ALGORITHM: str = 'HS256'
    ACESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    

    class Config:
        case_senstive = True


settings = Settings()