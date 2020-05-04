from app import create_app, db
from app.config import BaseConfig
import json
import os

with open(os.path.join(os.getcwd(), 'config.json'), 'r') as file:
    config = json.load(file)


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = config.get('database').get('testing_uri')


app = create_app(TestConfig)
app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()
app.run()
