from sqlalchemy import Column, ForeignKey, Boolean, Text
from sqlalchemy import Integer

from .meta import Base


class ReviewRating(Base):
    __tablename__ = 'review_rating'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Text, ForeignKey('user.email'))
    review_id = Column(Integer, ForeignKey('review.id'))
    value = Column(Boolean)

    def __init__(self, user_id, review_id, value):
        self.user_id = user_id
        self.review_id = review_id
        self.value = value
