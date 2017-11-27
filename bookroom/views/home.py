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
