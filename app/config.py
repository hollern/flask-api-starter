import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(os.getcwd(), 'config.json'), 'r') as file:
    config = json.load(file)


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEFAULT_TOKEN_EXPIRY = 8  # hours

    # Security
    SECRET_KEY = 'secret-key'
    JWT_SECRET_KEY = 'jwt-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'

    # Emailing
    SYSTEM_EMAIL = config.get('system_email')

    # Services
    SENDGRID_SECRET_KEY = config.get('services').get('sendgrid')


class DevConfig(BaseConfig):
    # Main
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config.get('database').get('development_uri')


class LiveConfig(BaseConfig):
    # Main
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = config.get('database').get('live_uri')

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY') or config.get('secrets').get('secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or config.get('secrets').get('jwt_secret_key')
    JWT_ERROR_MESSAGE_KEY = 'message'
