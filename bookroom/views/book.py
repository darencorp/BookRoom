import datetime

from pyramid.view import view_config
from sqlalchemy import desc, func, and_

from bookroom.models.User import User
from bookroom.models.BookRating import BookRating
from bookroom.models.Review import Review
from bookroom.models.ReviewRating import ReviewRating


class BookView(object):
    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession
        self.session = request.session
        self.settings = request.registry.settings

    @view_config(route_name='add_review', renderer='json', permission='view')
    def add_review(self):
        r = self.request
        j = r.json_body

        body = j.get('body')
        book_id = int(j.get('book'))
        user_id = r.authenticated_userid

        now = datetime.datetime.now().replace(microsecond=0)

        review = Review(user_id, book_id, body, now, False)

        self.DBSession.add(review)

        return dict()

    @view_config(route_name='update_reviews', renderer='json')
    def update_reviews(self):
        r = self.request
        _id = r.json_body

        try:
            id = int(_id)
        except ValueError:
            return dict()

        reviews_query = self.DBSession.query(Review.id, Review.body, Review._date, Review.modified, User.first_name,
                                             User.last_name, User.avatar).join(User,
                                                                               User.email == Review.user_id).filter(
            Review.book_id == id).order_by(desc(Review._date))

        reviews = [
            {
                'id': i.id,
                'body': i.body,
                'date': i._date.strftime("%Y-%m-%d %H:%M"),
                'modified': i.modified,
                'user_fname': i.first_name,
                'user_lname': i.last_name,
                'user_avatar': i.avatar
            } for i in reviews_query
        ]

        return dict(reviews=reviews)

    @view_config(route_name='vote_book', renderer='json', permission='view')
    def vote_book(self):
        r = self.request
        j = r.json_body

        _book_id = j.get('book_id')
        user_id = r.authenticated_userid
        rating = j.get('rating')

        try:
            book_id = int(_book_id)
        except ValueError:
            return dict()

        exist_rate = self.DBSession.query(BookRating).filter(
            and_(BookRating.user_id == user_id, BookRating.book_id == book_id)).first()

        if exist_rate:
            self.DBSession.query(BookRating).filter(
                and_(BookRating.user_id == user_id, BookRating.book_id == book_id)).update({"value": rating})
        else:
            book_rating = BookRating(user_id, book_id, rating)
            self.DBSession.add(book_rating)

        rate_query = self.DBSession.query(func.avg(BookRating.value)).filter(BookRating.book_id == book_id).first()
        avg_rating = int(rate_query[0])

        return dict(avg_rating=avg_rating)

    @view_config(route_name='vote_review', renderer='json', permission='view')
    def vote_review(self):
        r = self.request
        j = r.json_body

        _review_id = j.get('review_id')
        user_id = r.authenticated_userid
        rating = j.get('rating')

        try:
            review_id = int(_review_id)
        except ValueError:
            return dict()

        exist_rate = self.DBSession.query(ReviewRating).filter(
            and_(ReviewRating.user_id == user_id, ReviewRating.review_id == review_id)).first()

        if exist_rate:
            self.DBSession.query(ReviewRating).filter(
                and_(ReviewRating.user_id == user_id, ReviewRating.review_id == review_id)).update({"value": rating})
        else:
            review_rating = ReviewRating(user_id, review_id, rating)
            self.DBSession.add(review_rating)

        review_query = self.DBSession.query(Review.id, self.DBSession.query(func.count(ReviewRating.id)).filter(
            and_(ReviewRating.value == True,
                 ReviewRating.review_id == Review.id)).label('t_value'),
                                            self.DBSession.query(func.count(ReviewRating.id)).filter(
                                                and_(ReviewRating.value == False,
                                                     ReviewRating.review_id == Review.id)).label('f_value')).filter(
            Review.id == review_id).first()

        review = {
            'true_rating': review_query.t_value,
            'false_rating': review_query.f_value
        }

        return dict(review=review)
