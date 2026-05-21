from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    CORS_ORIGINS = [os.getenv('CORS_ORIGINS', '*'), 'http://localhost:5173']


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:postgres@localhost/dev_db').replace("postgres://", "postgresql://")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=180)


class ProdConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://dev_db_gwaq_user:qTds3t9bIxiP6ldhBK2CugN1Dv1dAEtU@dpg-d1655rbipnbc73fir470-a.frankfurt-postgres.render.com/dev_db_gwaq')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=180)
    API_URL = os.getenv('API_URL', 'https://ggforge-server.onrender.com')
