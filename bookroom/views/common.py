import re

from passlib.handlers.bcrypt import bcrypt
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config, forbidden_view_config
from bookroom.models import User


class Common(object):
    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession
        self.session = request.session

    @view_config(route_name='js', renderer='../templates/lib/js.html')
    def js(self):
        """Render JavaScript urls
        """
        # self.request.response.content_type = 'application/javascript'
        return dict()

    @view_config(route_name='index', renderer='../templates/index.html')
    def my_view(self):
        if self.session.get('loged_in'):
            return HTTPFound(location='login')
        return dict()

    @view_config(route_name='login', renderer='../templates/views/home/home.html')
    @forbidden_view_config(renderer='../templates/views/home/home.html')
    def go_login(self):

        def authenticate(email, password):
            user_query = self.DBSession.query(User).filter(User.email == email).limit(1)

            user = [{
                'first_name': i.first_name,
                'last_name': i.last_name,
                'email': i.email,
                'role': i.role
            } for i in user_query]

            my_password = [{
                'password': i.password
            } for i in user_query]

            if len(my_password) != 0 and bcrypt.verify(password, my_password[0].get('password')):
                return user[0]
            else:
                return False

        login_url = self.request.resource_url(self.request.context, 'login')
        message = ''
        login = self.request.POST.get('email')
        password = self.request.POST.get('password')

        if self.session.get('loged_in'):
            return dict()

        user = authenticate(login, password)

        if user:
            self.session['loged_in'] = self.request.create_jwt_token(user)
            return HTTPFound(location=login_url)
        else:
            message = 'Failed login'

        return HTTPFound(location='/')

    @view_config(route_name='register', renderer='json')
    def some(self):
        j = self.request.json_body

        if j.get('password') != j.get('confirmed_password') or len(j.get('password')) == 0:
            error_dict = {
                'code': 400,
                'desc': "Passwords is invalid"
            }
            return dict(error=error_dict)

        email_regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

        if not email_regex.match(j.get('email')):
            error_dict = {
                'code': 401,
                'desc': "Email is not valid"
            }

            return dict(error=error_dict)

        dbuser = self.DBSession.query(User).filter(User.email == j.get('email'))

        u = [{
            'email': i.email
        } for i in dbuser]

        if not len(u) == 0:
            error_dict = {
                'code': 402,
                'desc': "Email is used"
            }

            return dict(error=error_dict)

        user = User(j.get('first_name'), j.get('last_name'), j.get('email'), j.get('password'))

        self.DBSession.add(user)

        return dict()

    @view_config(route_name='logout', renderer='../templates/index.html')
    def logout(self):
        self.session['loged_in'] = None
        return HTTPFound(location=self.request.resource_url(self.request.context))
