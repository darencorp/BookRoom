from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text

from .meta import Base


class LibraryBook(Base):
    __tablename__ = 'library_book'
    id = Column(Integer, primary_key=True)
    owner = Column(Text)

    book_info = Column(ForeignKey('MarketBook.id'), nullable=False)
