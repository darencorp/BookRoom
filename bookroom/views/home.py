

class Home(object):

    def __init__(self, request):
        self.requet = request
        self.DBSession = request.dbsession
        self.session = request.session
