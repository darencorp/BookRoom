import re

from passlib.handlers.bcrypt import bcrypt
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, authenticated_userid
from pyramid.view import view_config, forbidden_view_config
from bookroom.models import User
from bookroom.models.facades.home_facade import HomeFacade


class Common(object):
    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession
        self.session = request.session

        self.hf = HomeFacade(request)

    @view_config(route_name='js', renderer='../templates/lib/js.html')
    def js(self):
        """Render JavaScript urls
        """
        return dict()

    @view_config(route_name='index', renderer='../templates/index.html')
    def my_view(self):
        if authenticated_userid(request=self.request):
            return HTTPFound(location='login')

        return dict()

    @view_config(route_name='home', renderer='../templates/index.html')
    def home(self):
        if not authenticated_userid(request=self.request):
            return HTTPFound(location='/')

        return dict()

    @view_config(route_name='login', renderer='json')
    @forbidden_view_config(renderer='json')
    def go_login(self):

        def authenticate(email, password):
            user_query = self.DBSession.query(User).filter(User.email == email).first()

            user = {
                'first_name': user_query.first_name,
                'last_name': user_query.last_name,
                'email': user_query.email
            }

            my_password = {
                'password': user_query.password
            }

            if len(my_password) != 0 and bcrypt.verify(password, my_password.get('password')):
                return user
            else:
                return False

        r = self.request

        if authenticated_userid(request=r):
            return HTTPFound(location=self.request.route_path('home'))

        p = self.request.json

        login = p.get('email', '')
        password = p.get('password', '')

        if login == '' or password == '':
            return dict(error="Email or password is incorrect!")

        user = authenticate(login, password)

        if user:
            self.session['loged_as'] = user
            remember(request=r, userid=user['email'])
            return dict()

        return dict(error="Email or password is incorrect!")

    @view_config(route_name='register', renderer='json')
    def register(self):
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

        u = [{'email': i.email} for i in dbuser]

        if not len(u) == 0:
            error_dict = {
                'code': 402,
                'desc': "Email is used"
            }

            return dict(error=error_dict)

        user = User(j.get('first_name'), j.get('last_name'), j.get('email'), j.get('password'))

        self.DBSession.add(user)

        login_user = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

        self.session['loged_as'] = login_user
        remember(request=self.request, userid=user['email'])

        return dict()

    @view_config(route_name='logout', renderer='json')
    def logout(self):
        self.session.clear()
        return HTTPFound(location=self.request.route_path('home'))
