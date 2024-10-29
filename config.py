from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from typing import List
import os

DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings (BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    host:           str
    cryptage:       str
    port:           str
    userlabel:      str
    emailname:      str
    domain:         str
    login:          str
    password:       str

settings = Settings()
