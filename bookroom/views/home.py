import os

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from bookroom.lib.helpers import fix_webasset

from bookroom.models import MarketBook
from bookroom.models.facades.home_facade import HomeFacade


class Home(object):

    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession
        self.session = request.session
        self.settings = request.registry.settings

        self.hf = HomeFacade(request)

    @view_config(route_name='upload', renderer='json')
    def upload(self):

        path = fix_webasset(self.settings.get('webassets.base_dir')) + '/img/books/'

        books = self.DBSession.query(MarketBook).all()

        items = []

        for b in books:
            items.append({
                'id': b.id,
                'image': b.image
            })

        path = []

        for i in items:
            some = i['image'].rsplit('/')
            path.append({
                'image': some[-1],
                'id': i['id']
            })
        for i in path:
            p = '../../../static/img/books/' + i['image']
            self.DBSession.query(MarketBook).filter_by(id=i['id']).update({'image': p})

        # book = MarketBook(path, r.get('name'), r.get('author'), r.get('category'), r.get('price'))
        # self.DBSession.add(book)

        return HTTPFound(location='/')

    @view_config(route_name='book', renderer='json')
    def book(self):
        id_ = self.request.matchdict.get('id')

        item = self.hf.by_id(id_)

        book = {
            'id': item.id,
            'image': item.image,
            'name': item.name,
            'price': item.price,
            'desc': item.description
        }

        return dict(book=book)