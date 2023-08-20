from flask import jsonify

from .base_command import BaseCommand
from ..errors.errors import no_offer_found
from ..models.model import db_session, init_db
from ..models.offer import Offer

DELETE = 'DELETE'

init_db()


class OffersOperations(BaseCommand):

    def __init__(self, post_id=None,
                 user_id=None,
                 offer_id=None,
                 operation=None):
        """

        :type post_id: object
        """
        self.post_id = post_id
        self.user_id = user_id
        self.offer_id = offer_id
        self.operation = operation

    @property
    def get_offer_by_user_and_post(self):

        if self.post_id is None and not self.user_id == None:
            return Offer.query.filter_by(userId=self.user_id).all()
        if not self.user_id is None and not self.post_id is None:
            return Offer.query.filter_by(userId=self.user_id, postId=self.post_id).all()

        offer_list = Offer.query.all()
        return offer_list

    def get_offer_by_id(self):
        return Offer.query.filter_by(id=self.offer_id).first()

    def delete_offer(self):
        offer = self.get_offer_by_id()
        if not offer:
            raise no_offer_found
        db_session.delete(offer)
        db_session.commit()
        return True

    def reset(self):
        try:

            db_session.query(Offer).delete()
            db_session.commit()

            return jsonify({"msg": "Todos los datos fueron eliminados"}), 200
        except Exception as e:
            db_session.rollback()
            return jsonify({"message": "An error occurred while deleting offers"}), 500

    def execute(self):
        if not self.offer_id is None and not self.operation == DELETE:
            return self.get_offer_by_id()
        if self.operation == DELETE:
            return self.delete_offer()
        if self.operation == 'RESET':
            return self.reset()
        return self.get_offer_by_user_and_post
