from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy import Integer

from .meta import Base


class ReviewRating(Base):
    __tablename__ = 'review_rating'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    review_id = Column(Integer, ForeignKey('review.id'))
    value = Column(Boolean)

    def __init__(self, user_id, book_id, value):
        self.user_id = user_id
        self.book_id = book_id,
        self.value = value
