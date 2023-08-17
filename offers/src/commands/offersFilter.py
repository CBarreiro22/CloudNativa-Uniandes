from src.commands.base_command import BaseCommand
from src.models.model import Offer, db


class OffersFilter(BaseCommand):

    def __init__(self, post_id, user_id, no_user,no_post_id):
        self.post_id = post_id
        self.user_id = user_id
        self.no_user = no_user
        self.no_post_id = no_post_id

    def get_offer_by_user_and_post(self):

        if self.no_user and not self.no_post_id:
            return Offer.query.filter_by(postId=self.post_id).all()
        if not self.no_user or not self.no_post_id:
            return Offer.query.filter_by(userId=self.user_id, postId=self.post_id).all()

        offer_list = Offer.query.all()
        return offer_list

    def execute(self):
        print("entre a offers filter")
        return self.get_offer_by_user_and_post()
