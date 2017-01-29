from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text

from .meta import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    password = Column(Text)
    role = Column(Text)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.encrypt(password)
        self.role = 'user'

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)
