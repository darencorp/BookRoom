import bcrypt
from pyramid.security import Allow, ALL_PERMISSIONS

from bookroom.models import User


def hash_password(pw):
    hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
    # return unicode instead of bytes because databases handle it better
    return hashed_pw.decode('utf-8')


def check_password(expected_hash, pw):
    if expected_hash is not None:
        return bcrypt.checkpw(pw.encode('utf-8'), expected_hash.encode('utf-8'))
    return False


def groupfinder(user_mail, request):
    users_query = request.dbsession.query(User.id, User.role).filter(User.email == user_mail).first()

    user_role = {
        'role': users_query.role
    }

    if user_role:
        return [user_role['role']]


class Root(object):
    __acl__ = [
        (Allow, 'user', 'view'),
        (Allow, 'admin', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        self.request = request
