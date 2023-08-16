from dotenv import load_dotenv
import logging
import os
class Config(object):
    def __init__(self, env_file=".env"):
        self.env_file = env_file
        logging.info("loading env")
        self.load_env()

    def load_env(self):
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)

    def get(self, key, default=None):
        return os.getenv(key, default)

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