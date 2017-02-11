import datetime
from sqlalchemy import Column, Date, ForeignKey, Integer, Text
from sqlalchemy import DateTime

from bookroom.models.meta import Base


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, nullable=False)
    owner = Column(ForeignKey('user.email'), nullable=False)
    content = Column(Text)
    added = Column(DateTime, default=None)
    modified = Column(DateTime, default=None)