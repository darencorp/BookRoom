import datetime

import os

import sys

import shutil
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from bookroom.models.facades.home_facade import HomeFacade
from models.Book import Book


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
        if not self.request.is_xhr:
            return dict()

        return dict()

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
