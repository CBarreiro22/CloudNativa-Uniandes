import os
from dotenv import load_dotenv, find_dotenv

os.environ['ENV'] = 'test'


def pytest_configure(config):
    env_file = find_dotenv('./.env.test')
    load_dotenv(env_file)
    print("ENV:", os.environ['ENV'])
    return config
