# app/core/config.py
from pydantic_settings import BaseSettings
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import ConfigDict



# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)


class Settings(BaseSettings):
    instagram_access_token: str
    instagram_account_id: str
    facebook_app_id: str
    facebook_app_secret: str

    model_config = ConfigDict(env_file=".env")

settings = Settings()
