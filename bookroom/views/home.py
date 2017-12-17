import datetime

import os

import sys

import shutil
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import func, desc
from sqlalchemy.dialects.postgresql import array

from bookroom.models.facades.home_facade import HomeFacade
from bookroom.models.Book import Book
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

        if not self.request.is_xhr:
            return dict()

        return dict()

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

        book_query = self.DBSession.query(Book).filter(Book.id == id).first()

        reviews_query = self.DBSession.query(Review.id, Review.body, Review._date, Review.modified, User.first_name,
                                             User.last_name).join(User, User.email == Review.user_id).filter(
            Review.book_id == id).order_by(desc(Review._date))

        book = {
            'id': book_query.id,
            'name': book_query.name,
            'author': book_query.author,
            'year': book_query.year,
            'genre': book_query.genre,
            'desc': book_query.description,
            'image': book_query.image
        }

        reviews = [
            {
                'id': i.id,
                'body': i.body,
                'date': i._date.strftime("%Y-%m-%d %H:%M"),
                'modified': i.modified,
                'user_fname': i.first_name,
                'user_lname': i.last_name
            } for i in reviews_query
        ]

        return dict(book=book, reviews=reviews)

    @view_config(route_name='add_book', renderer='json')
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

    @view_config(route_name='image_upload', renderer='json')
    def image_upload(self):
        p = self.request.POST

        image = p.get('image')
        name = p.get('name')

        if image == None:
            return dict('')

        file_type = image.filename.split('.')[-1]

        current_date = str(datetime.datetime.now()).replace('.', '').replace(' ', '').replace(':', '')

        filename = '{0}{1}.{2}'.format(current_date, name, file_type).replace(' ', '')
        file = image.file
        filepath = str(os.path.dirname(__file__)) + '/../static/img/books/'

        with open(filepath + filename, 'wb') as output_file:
            shutil.copyfileobj(file, output_file)

        return filename

    @view_config(route_name='add_review', renderer='json')
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
                                             User.last_name).join(User, User.email == Review.user_id).filter(Review.book_id == id).order_by(desc(Review._date))

        reviews = [
            {
                'id': i.id,
                'body': i.body,
                'date': i._date.strftime("%Y-%m-%d %H:%M"),
                'modified': i.modified,
                'user_fname': i.first_name,
                'user_lname': i.last_name
            } for i in reviews_query
        ]

        return dict(reviews=reviews)
