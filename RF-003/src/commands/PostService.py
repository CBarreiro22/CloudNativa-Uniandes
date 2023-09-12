import os
from abc import ABC

from .BaseCommand import BaseCommand

POSTS_PATH = os.environ["POSTS_PATH"]
class PostsService(BaseCommand):

