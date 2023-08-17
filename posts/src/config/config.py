import logging
import os

from dotenv import load_dotenv


class Config(object):
    def __init__(self, env_file):
        self.env_file = env_file
        logging.info("loading env")
        self.load_env()
        # Configure the root logger
        logging.basicConfig(level=logging.DEBUG,  # Set the minimum log level
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename='app.log',  # Log to a file
                            filemode='w')

    def load_env(self):
        if os.path.exists(self.env_file):
            load_dotenv(dotenv_path=self.env_file)

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