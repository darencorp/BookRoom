from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from bookroom.models.facades.home_facade import HomeFacade


class Home(object):
    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession
        self.session = request.session
        self.settings = request.registry.settings

        self.hf = HomeFacade(request)

    @view_config(route_name='catalogue', renderer='../templates/views/catalogue.html')
    @view_config(route_name='catalogue', xhr=True, renderer='json')
    def catalogue(self):
        if not self.request.is_xhr:
            return dict()

        return dict()

    @view_config(route_name='user', renderer='../templates/views/user-page.html')
    @view_config(route_name='user', xhr=True, renderer='json')
    def user(self):

        if not self.request.is_xhr:
            return dict()

        return dict()

    @view_config(route_name='small_search', renderer='json')
    def small_search(self):
        return dict()

    @view_config(route_name='global_search', renderer='../templates/views/search.html')
    @view_config(route_name='global_search', xhr=True, renderer='json')
    def global_search(self):
        if not self.request.is_xhr:
            return dict()

        return dict()

    @view_config(route_name='get_book', renderer='../templates/views/book.html')
    @view_config(route_name='get_book', xhr=True, renderer='json')
    def get_book(self):
        if not self.request.is_xhr:
            return dict()

        return dict()
