import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    FLASK_APP = os.getenv('FLASK_APP', 'yacut')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'MY_SECRET_KEY')
