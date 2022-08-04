import os
#from dotenv import load_dotenv

#load_dotenv()

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') + os.environ.get('DATABASE_NAME')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_SQLITE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
