from pyramid.view import view_config

from bookroom.models import MarketBook


class Common(object):
    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession

    @view_config(route_name='js', renderer='../templates/lib/js.html')
    def js(self):
        """Render JavaScript urls
        """
        # self.request.response.content_type = 'application/javascript'
        return dict()

    @view_config(route_name='index', renderer='../templates/index.html')
    def my_view(self):
        return dict()

    @view_config(route_name='home', renderer='../templates/views/home/home.html')
    def go_login(self):
        return dict()

    @view_config(route_name='some', renderer='json')
    def some(self):
        return dict()
