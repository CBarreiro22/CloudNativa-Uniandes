import os
from abc import ABC

import requests
from dotenv import load_dotenv

from marshmallow import Schema, fields

from .BaseCommand import BaseCommand
from ..erros.errors import internal_server_error

loaded = load_dotenv('.env.development')

POSTS_PATH = os.environ["POSTS_PATH"]


class PostsService(BaseCommand, ABC):

    @staticmethod
    def post(post, headers):
        schema = PostJsonSchema()
        json_post = schema.dump(post)
        response = requests.post(url=f"{POSTS_PATH}/posts", json=json_post, headers=headers)
        return response.json(), response.status_code




class Post:

    def __init__(self, routeId, expireAt):
        """
        :param routeId:
        :param expireAt:
        :return:
        """
        self.routeId = routeId
        self.expireAt = expireAt


class PostJsonSchema(Schema):
    routeId = fields.String()
    expireAt = fields.String()
