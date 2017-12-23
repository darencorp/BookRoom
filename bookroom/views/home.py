import datetime
import os
import shutil

from passlib.handlers.bcrypt import bcrypt
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import func, desc, and_
from bookroom.models.facades.home_facade import HomeFacade
from bookroom.models.Book import Book
from models.BookRating import BookRating
from models.RaviewRating import ReviewRating
from models.User import User
from models.Review import Review


class Home(object):
    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession
        self.session = request.session
        self.settings = request.registry.settings

        self.hf = HomeFacade(request)

    @view_config(route_name='catalogue', renderer='../templates/views/catalogue.html')
    def catalogue(self):
        return dict()

    @view_config(route_name='get_catalogue', renderer='json')
    def get_catalogue(self):
        book_query = self.DBSession.query(Book).all()

        books = [
            {
                'id': i.id,
                'name': i.name,
                'author': i.author,
                'year': i.year,
                'genre': i.genre,
                'desc': i.description,
                'image': i.image
            } for i in book_query
        ]

        return dict(books=books)

    @view_config(route_name='user', renderer='../templates/views/user-page.html')
    @view_config(route_name='user', xhr=True, renderer='json')
    def user(self):

        m = self.request.matchdict

        _id = m.get('id')

        try:
            id = int(_id)
        except ValueError:
            return HTTPNotFound()

        if not self.request.is_xhr:
            return dict(id=id)

        user_query = self.DBSession.query(User).filter(User.id == id).first()

        book_query = self.DBSession.query(BookRating, Book).join(User, User.id == id).join(Book,
                                                                                           BookRating.book_id == Book.id).filter(
            BookRating.user_id == User.email)

        book_reviews_query = self.DBSession.query(Review, Book).join(Book, Book.id == Review.book_id).join(User,
                                                                                                           User.email == Review.user_id).filter(
            User.id == id)

        user = {
            'first_name': user_query.first_name,
            'last_name': user_query.last_name,
            'image': user_query.avatar,
            'email': user_query.email
        }

        book_stared = [
            {
                'id': i.Book.id,
                'name': i.Book.name,
                'author': i.Book.author,
                'image': i.Book.image,
                'desc': i.Book.description,
                'rating': i.BookRating.value
            } for i in book_query
        ]

        book_reviews = dict()

        for i in book_reviews_query:
            if not book_reviews.get(i.Book.id):
                book_reviews[i.Book.id] = dict()

            if book_reviews[i.Book.id].get('reviews'):
                book_reviews[i.Book.id]['reviews'].append({
                    'body': i.Review.body,
                    'date': i.Review._date.strftime("%Y-%m-%d %H:%M")})
            else:
                book_reviews[i.Book.id]['reviews'] = [{
                    'body': i.Review.body,
                    'date': i.Review._date.strftime("%Y-%m-%d %H:%M")
                }]

            book_reviews[i.Book.id]['id'] = i.Book.id
            book_reviews[i.Book.id]['name'] = i.Book.name
            book_reviews[i.Book.id]['author'] = i.Book.author
            book_reviews[i.Book.id]['image'] = i.Book.image

        for k, v in book_reviews.items():
            v['reviews'].sort(key=lambda x: x['date'], reverse=True)

        return dict(user=user, book_stared=book_stared, book_reviews=book_reviews)

    @view_config(route_name='small_search', renderer='json')
    def small_search(self):
        return dict()

    @view_config(route_name='global_search', renderer='../templates/views/search.html')
    @view_config(route_name='global_search', xhr=True, renderer='json')
    def global_search(self):
        if not self.request.is_xhr:
            return dict()

        return dict()

    @view_config(route_name='get_book', renderer='../templates/views/book.html')
    @view_config(route_name='get_book', xhr=True, renderer='json')
    def get_book(self):

        r = self.request
        _id = r.matchdict.get('id')

        try:
            id = int(_id)
        except ValueError:
            return HTTPNotFound()

        if not self.request.is_xhr:
            book_id = self.DBSession.query(Book.id).filter(Book.id == id).first().id
            return dict(book_id=book_id)

        def get_user_review_rating(review_id):
            user_rating = self.DBSession.query(ReviewRating.value).filter(
                and_(ReviewRating.review_id == review_id, ReviewRating.user_id == r.authenticated_userid)).first()

            return user_rating.value if user_rating else None

        book_query = self.DBSession.query(Book).filter(Book.id == id).first()

        reviews_query = self.DBSession.query(
            Review, User,
            self.DBSession.query(func.count(ReviewRating.id)).filter(
                and_(ReviewRating.value == True, ReviewRating.review_id == Review.id)).label('t_value'),
            self.DBSession.query(func.count(ReviewRating.id)).filter(
                and_(ReviewRating.value == False, ReviewRating.review_id == Review.id)).label('f_value')) \
            .join(User,
                  User.email == Review.user_id).filter(
            Review.book_id == id).order_by(desc(Review._date)).all()

        rate_query = self.DBSession.query(func.avg(BookRating.value)).filter(BookRating.book_id == id).first()

        avg_rating = int(rate_query[0]) if rate_query[0] else 0

        u_rate = None

        reviews = [
            {
                'id': i.Review.id,
                'body': i.Review.body,
                'date': i.Review._date.strftime("%Y-%m-%d %H:%M"),
                'modified': i.Review.modified,
                'user_fname': i.User.first_name,
                'user_lname': i.User.last_name,
                'user_avatar': i.User.avatar,
                'user_id': i.User.id,
                'true_rating': i.t_value,
                'false_rating': i.f_value
            } for i in reviews_query
        ]

        if r.authenticated_userid:
            exist_rate = self.DBSession.query(BookRating).filter(
                and_(BookRating.user_id == r.authenticated_userid, BookRating.book_id == id)).first()

            if exist_rate:
                u_rate = exist_rate.value

            for i in reviews:
                i['user_vote'] = get_user_review_rating(i['id'])

        book = {
            'id': book_query.id,
            'name': book_query.name,
            'author': book_query.author,
            'year': book_query.year,
            'genre': book_query.genre,
            'desc': book_query.description,
            'image': book_query.image
        }

        user_rate = u_rate if u_rate else False

        return dict(book=book, reviews=reviews, user_rating=user_rate, avg_rating=avg_rating)

    @view_config(route_name='add_book', renderer='json', permission='admin')
    def add_book(self):
        r = self.request
        j = r.json

        name = j['name']
        author = j.get('author')
        year = j.get('year', 0)
        genre = j.get('genre')
        description = j.get('description')
        image = j.get('image')

        book = Book(name, author, year, genre, description, image)

        self.DBSession.add(book)
        return dict()

    @view_config(route_name='image_upload', renderer='json', permission='admin')
    def image_upload(self):
        p = self.request.POST

        image = p.get('image')
        name = p.get('name')

        if image is None:
            return dict('')

        file_type = image.filename.split('.')[-1]

        current_date = str(datetime.datetime.now()).replace('.', '').replace(' ', '').replace(':', '')

        filename = '{0}{1}.{2}'.format(current_date, name, file_type).replace(' ', '')
        file = image.file
        filepath = str(os.path.dirname(__file__)) + '/../static/img/books/'

        with open(filepath + filename, 'wb') as output_file:
            shutil.copyfileobj(file, output_file)

        return filename

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

        sorted_reviews = sorted(reviews.keys(), key=lambda x: x, reverse=True)

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

    @view_config(route_name='avatar_change', renderer='json', permission='view')
    def avatar_change(self):
        p = self.request.POST

        image = p.get('image')

        if image is None:
            return dict(success=False)

        file_type = image.filename.split('.')[-1]

        current_date = str(datetime.datetime.now()).replace(':', '').replace(' ', '').replace('.', '')

        filename = '{0}{1}.{2}'.format(current_date,
                                       self.request.authenticated_userid.replace('.', '_').replace('@', '-'), file_type)
        file = image.file
        filepath = str(os.path.dirname(__file__)) + '/../static/img/users/'

        user_image = self.DBSession.query(User.avatar).filter(User.email == self.request.authenticated_userid).first()[
            0]

        if user_image:
            os.remove(filepath + user_image)

        with open(filepath + filename, 'wb') as output_file:
            shutil.copyfileobj(file, output_file)

        self.DBSession.query(User).filter(User.email == self.request.authenticated_userid).update({"avatar": filename})

        return dict(success=True, image=filename)

    @view_config(route_name='change_data', renderer='json', permission='view')
    def change_data(self):
        j = self.request.json_body

        fname = j.get('fname')
        lname = j.get('lname')

        self.DBSession.query(User).filter(User.email == self.request.authenticated_userid).update(
            {'first_name': fname, 'last_name': lname})

        self.session['logged_as']['first_name'] = fname
        self.session['logged_as']['last_name'] = lname

        return dict()

    @view_config(route_name='change_password', renderer='json', permission='view')
    def change_password(self):
        j = self.request.json_body

        user_password = self.DBSession.query(User).filter(
            User.email == self.request.authenticated_userid).first().password

        if not bcrypt.verify(j['old_password'], user_password):
            return dict(error='Old password is incorrect!')

        if not j['new_password'] or not j['confirm_password']:
            return dict(error='Passwords are invalid!')

        if not j['new_password'] == j['confirm_password']:
            return dict(error='Passwords are invalid!')

        self.DBSession.query(User).filter(User.email == self.request.authenticated_userid).update(
            {'password': bcrypt.encrypt(j['confirm_password'])})

        return dict()
