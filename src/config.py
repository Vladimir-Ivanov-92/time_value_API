import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# JWT secret key
SECRET_JWT = os.environ.get("SECRET_JWT")

# Auth manager secret key
SECRET_AUTH_MANAGER_KEY = os.environ.get("SECRET_AUTH_MANAGER_KEY")
