from pyramid.view import view_config


class Common(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='home', renderer='../templates/index.html')
    def my_view(self):
        return dict()
