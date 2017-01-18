from pyramid.view import view_config


class Common(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='js', renderer='../templates/lib/js.html')
    def js(self):
        """Render JavaScript urls
        """
        self.request.response.content_type = 'application/javascript'
        return dict()

    @view_config(route_name='home', renderer='../templates/index.html')
    def my_view(self):
        return dict()
