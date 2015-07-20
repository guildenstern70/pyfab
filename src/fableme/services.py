import webapp2
import fableme.db.schema
import logging


class LikeItHandler(webapp2.RequestHandler):

    def post(self):
        logging.debug("Like IT POST called.")
        review_id = self.request.get('review_id')
        email_user = self.request.get('like_mail')
        nr_of_likes = fableme.db.schema.DbFableReview.like_it(review_id, email_user)
        self.response.write('{ "likes": "XXX" }'.replace('XXX', str(nr_of_likes)))
