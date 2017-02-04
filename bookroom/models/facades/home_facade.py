from sqlalchemy import and_

from bookroom.models import MarketBook, LibraryBook

class HomeFacade(object):

    def __init__(self, request):
        self.DBSession = request.dbsession
        self.request = request
        self.session = request.session

    def get_all_marketbooks(self):
        return self.DBSession.query(MarketBook).all()

    def marketbook_by_id(self, id):
        id_ = int(id) if id else 0

        return self.DBSession.query(MarketBook).filter(MarketBook.id == id_).first()

    def add_library_book(self, id):

        ret = None

        if id:
            book = LibraryBook(self.session['loged_as'].get('email'), id)
            ret = self.DBSession.add(book)

        return ret

    def get_library_book_by_key(self, book_id, owner):
        return self.DBSession.query(LibraryBook).filter(and_(LibraryBook.owner == owner, LibraryBook.book_info == book_id)).first()

    def get_library(self):
        return self.DBSession.query(LibraryBook, MarketBook.name, MarketBook.description, MarketBook.author, MarketBook.image).\
            join(MarketBook, MarketBook.id == LibraryBook.book_info).\
            filter(LibraryBook.owner == self.session['loged_as'].get('email')).all()