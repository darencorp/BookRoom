from bookroom.models import MarketBook


class HomeFacade(object):

    def __init__(self, request):
        self.DBSession = request.dbsession
        self.request = request

    def get_all_marketbooks(self):
        return self.DBSession.query(MarketBook).all()

    def by_id(self, id):
        id_ = int(id) if id else 0

        return self.DBSession.query(MarketBook).filter(MarketBook.id == id_).first()
