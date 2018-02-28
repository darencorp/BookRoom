import datetime

import os

import shutil
import transaction
from pyramid.view import view_config

from bookroom.models.Book import Book
from bookroom.models.BookRating import BookRating
from bookroom.models.Review import Review
from bookroom.models.ReviewRating import ReviewRating


class AdminView(object):
    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession
        self.session = request.session
        self.settings = request.registry.settings

    @view_config(route_name='add_book', request_method='POST', renderer='json', permission='admin')
    def add_book(self):
        r = self.request
        j = r.json

        name = j['name']
        author = j.get('author')
        year = j.get('year', 0)
        genre = j.get('genre')
        description = j.get('desc')
        image = j.get('image')

        _id = j.get('id', None)

        if _id:
            book = self.DBSession.query(Book).filter(Book.id == _id).first()

            if book:
                self.DBSession.query(Book).filter(Book.id == _id).\
                    update({"name": name, "author": author, "year": year, "genre": genre, "description": description, "image": image})

        else:
            book = Book(name, author, year, genre, description, image)
            self.DBSession.add(book)

        return dict(id=_id)

    @view_config(route_name='image_upload', request_method='POST', renderer='json', permission='admin')
    def image_upload(self):
        p = self.request.POST

        image = p.get('image')
        name = p.get('name')
        _id = p.get('id', None)

        if image is None:
            return dict('')

        if type(image) is str:
            return image

        if _id:
            book = self.DBSession.query(Book).filter(Book.id == _id).first()

            if book:
                book_image = book.image
                filename = str(os.path.dirname(__file__)) + '/../static/img/books/' + book_image

                if os.path.isfile(filename):
                    os.remove(filename)

        file_type = image.filename.split('.')[-1]

        current_date = str(datetime.datetime.now()).replace('.', '').replace(' ', '').replace(':', '')

        filename = '{0}{1}.{2}'.format(current_date, name, file_type).replace(' ', '')
        file = image.file
        filepath = str(os.path.dirname(__file__)) + '/../static/img/books/'

        with open(filepath + filename, 'wb') as output_file:
            shutil.copyfileobj(file, output_file)

        return filename

    @view_config(route_name='update_book', request_method='POST', renderer='json', permission='admin')
    def update_book(self):
        return dict()

    @view_config(route_name='delete_book', request_method='POST', renderer='json', permission='admin')
    def delete_book(self):
        r = self.request
        _id = int(r.matchdict.get('id', None))

        if not _id:
            return False

        book = self.DBSession.query(Book).filter(Book.id == _id).first()

        if book:
            book_image = book.image
            filename = str(os.path.dirname(__file__)) + '/../static/img/books/' + book_image

            if os.path.isfile(filename):
                os.remove(filename)

                with transaction.manager:
                    self.DBSession.delete(book)

        return True
