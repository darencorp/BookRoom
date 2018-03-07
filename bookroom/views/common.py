import re

from passlib.handlers.bcrypt import bcrypt
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, authenticated_userid
from pyramid.view import view_config, forbidden_view_config
from sqlalchemy import desc, func

from bookroom.models import User
from bookroom.models.facades.home_facade import HomeFacade
from bookroom.models.Book import Book
from bookroom.models.BookRating import BookRating
from bookroom.models.Review import Review
from bookroom.models.ReviewRating import ReviewRating


class CommonView(object):
    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession
        self.session = request.session

        self.hf = HomeFacade(request)

    @view_config(route_name='js', renderer='../templates/lib/js.html')
    def js(self):
        """Render JavaScript urls
        """
        return dict()

    @view_config(route_name='index', renderer='../templates/index.html')
    @view_config(route_name='index', xhr=True, renderer='json')
    def index(self):
        r = self.request

        if not r.is_xhr:
            return dict()

        book_query = self.DBSession.query(Book, func.avg(BookRating.value).label("value")).join(BookRating,
                                                                                                BookRating.book_id == Book.id).group_by(
            Book.id).order_by(desc("value")).first()

        book = {
            'id': book_query.Book.id,
            'name': book_query.Book.name,
            'author': book_query.Book.author,
            'year': book_query.Book.year,
            'desc': book_query.Book.description,
            'image': book_query.Book.image,
            'rating': str(int(book_query.value))
        }

        review_query = self.DBSession.query(Review, Book, User, func.sum(ReviewRating.value).label("value"))\
            .join(Book, Book.id == Review.book_id)\
            .join(User, User.email == Review.user_id)\
            .join(ReviewRating, ReviewRating.review_id == Review.id)\
            .group_by(Review.id)\
            .order_by(desc("value"))\
            .limit(3)

        reviews = [
            {
                'body': i.Review.body,
                'modified': i.Review.modified,
                'date': i.Review._date.strftime("%Y-%m-%d %H:%M"),
                'book_id': i.Book.id,
                'book_name': i.Book.name,
                'user_id': i.User.id,
                'user_fname': i.User.first_name,
                'user_lname': i.User.last_name,
                'user_avatar': i.User.avatar
            } for i in review_query
        ]

        return dict(book=book, reviews=reviews)

    @view_config(route_name='about', renderer='../templates/views/about.html')
    def about(self):
        return dict()

    @view_config(route_name='login', renderer='json')
    @forbidden_view_config(renderer='json')
    def ogin(self):

        def authenticate(email, password):

            email_query = self.DBSession.query(User.email).filter(User.email == email).first()

            db_email = email_query

            if not db_email:
                return False

            user_query = self.DBSession.query(User).filter(User.email == email).first()

            user = {
                'id': user_query.id,
                'first_name': user_query.first_name,
                'last_name': user_query.last_name,
                'email': user_query.email
            }

            my_password = {
                'password': user_query.password
            }

            if len(my_password) != 0 and bcrypt.verify(password, my_password.get('password')):
                return user
            else:
                return False

        r = self.request

        if authenticated_userid(request=r):
            return HTTPFound(location=self.request.route_path('index'))

        p = self.request.json

        login = p.get('email', '')
        password = p.get('password', '')

        if login == '' or password == '':
            return dict(error="Email or password is incorrect!")

        user = authenticate(login, password)

        if user:
            self.session['logged_as'] = user
            remember(request=r, userid=user['email'])
            return dict()

        return dict(error="Email or password is incorrect!")

    @view_config(route_name='register', renderer='json')
    def register(self):
        j = self.request.json_body

        if j.get('password') is None or j.get('confirmed_password') is None:
            error_dict = {
                'code': 400,
                'desc': "Passwords are invalid"
            }
            return dict(error=error_dict)

        if j.get('password') != j.get('confirmed_password') or len(j.get('password')) == 0:
            error_dict = {
                'code': 400,
                'desc': "Passwords are invalid"
            }
            return dict(error=error_dict)

        email_regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

        if not email_regex.match(j.get('email')):
            error_dict = {
                'code': 401,
                'desc': "Email is not valid"
            }

            return dict(error=error_dict)

        dbuser = self.DBSession.query(User).filter(User.email == j.get('email'))

        u = [{'email': i.email} for i in dbuser]

        if not len(u) == 0:
            error_dict = {
                'code': 402,
                'desc': "Email is used"
            }

            return dict(error=error_dict)

        user = User(j.get('first_name'), j.get('last_name'), j.get('email'), j.get('password'))

        self.DBSession.add(user)

        login_user_query = self.DBSession.query(User.id, User.last_name, User.last_name, User.email).filter(
            User.email == j.get('email')).first()

        login_user = {
            'id': login_user_query.id,
            'first_name': login_user_query.first_name,
            'last_name': login_user_query.last_name,
            'email': login_user_query.email
        }

        self.session['logged_as'] = login_user
        remember(request=self.request, userid=login_user['email'])

        return dict()

    @view_config(route_name='logout', renderer='json')
    def logout(self):
        self.session.clear()
        return HTTPFound(location=self.request.referer)
