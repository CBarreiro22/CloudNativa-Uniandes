import logging
import os
class Config(object):
    DEBUG = False
    TESTING = False
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    logging.info("varialbes cargadas")
    logging.debug(f'SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}')

class ProductionConfig(Config):
    DEBUG = False
class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
class TestingConfig(Config):
    TESTING = True