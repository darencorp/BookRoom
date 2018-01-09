import datetime

import shutil

import os
from passlib.handlers import bcrypt
from pyramid.view import view_config

from bookroom.models import User


class UserView(object):
    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession
        self.session = request.session
        self.settings = request.registry.settings

    @view_config(route_name='avatar_change', renderer='json', permission='view')
    def avatar_change(self):
        p = self.request.POST

        image = p.get('image')

        if image is None:
            return dict(success=False)

        file_type = image.filename.split('.')[-1]

        current_date = str(datetime.datetime.now()).replace(':', '').replace(' ', '').replace('.', '')

        filename = '{0}{1}.{2}'.format(current_date,
                                       self.request.authenticated_userid.replace('.', '_').replace('@', '-'), file_type)
        file = image.file
        filepath = str(os.path.dirname(__file__)) + '/../static/img/users/'

        user_image = self.DBSession.query(User.avatar).filter(User.email == self.request.authenticated_userid).first()[
            0]

        if user_image:
            os.remove(filepath + user_image)

        with open(filepath + filename, 'wb') as output_file:
            shutil.copyfileobj(file, output_file)

        self.DBSession.query(User).filter(User.email == self.request.authenticated_userid).update({"avatar": filename})

        return dict(success=True, image=filename)

    @view_config(route_name='change_data', renderer='json', permission='view')
    def change_data(self):
        j = self.request.json_body

        fname = j.get('fname')
        lname = j.get('lname')

        self.DBSession.query(User).filter(User.email == self.request.authenticated_userid).update(
            {'first_name': fname, 'last_name': lname})

        self.session['logged_as']['first_name'] = fname
        self.session['logged_as']['last_name'] = lname

        return dict()

    @view_config(route_name='change_password', renderer='json', permission='view')
    def change_password(self):
        j = self.request.json_body

        user_password = self.DBSession.query(User).filter(
            User.email == self.request.authenticated_userid).first().password

        if not bcrypt.verify(j['old_password'], user_password):
            return dict(error='Old password is incorrect!')

        if not j['new_password'] or not j['confirm_password']:
            return dict(error='Passwords are invalid!')

        if not j['new_password'] == j['confirm_password']:
            return dict(error='Passwords are invalid!')

        self.DBSession.query(User).filter(User.email == self.request.authenticated_userid).update(
            {'password': bcrypt.encrypt(j['confirm_password'])})

        return dict()
