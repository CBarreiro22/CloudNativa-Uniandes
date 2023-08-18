from src.commands.base_command import BaseCommand
from src.models.model import Offer, db


class OffersFilter(BaseCommand):

    def __init__(self, post_id = None, user_id =None,offer_id=None):
        self.post_id = post_id
        self.user_id = user_id
        self.offer_id = offer_id

    @property
    def get_offer_by_user_and_post(self):

        if self.post_id is None and not self.user_id == None:
            return Offer.query.filter_by(userId=self.user_id).all()
        if not self.user_id is None and not self.post_id is None:
            return Offer.query.filter_by(userId=self.user_id, postId=self.post_id).all()

        offer_list = Offer.query.all()
        return offer_list
    def get_offer_by_id(self):
        return Offer.query.filter_by (id= self.offer_id).first()
    def execute(self):
        if not self.offer_id is None:
            return self.get_offer_by_id()
        return self.get_offer_by_user_and_post
