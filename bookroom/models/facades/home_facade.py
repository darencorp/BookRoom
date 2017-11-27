class HomeFacade(object):

    def __init__(self, request):
        self.DBSession = request.dbsession
        self.request = request
        self.session = request.session