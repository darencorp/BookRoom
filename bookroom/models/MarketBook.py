from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Binary
)
from sqlalchemy import Float

from .meta import Base


class MarketBook(Base):
    __tablename__ = 'market_book'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text)
    image = Column(Text)
    author = Column(Text)
    category = Column(Text)
    price = Column(Float)
    description = Column(Text)

    def __init__(self, image, name, author, category, price):
        self.image = image
        self.name = name
        self.author = author
        self.category = category
        self.price = price