from datetime import datetime
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from bookroom.lib.helpers import fix_webasset

from bookroom.models import MarketBook, Post
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
        id_ = int(self.request.matchdict.get('id'))

        item = self.hf.marketbook_by_id(id_)

        book = {
            'id': item.id,
            'image': item.image,
            'name': item.name,
            'price': item.price,
            'desc': item.description
        }

        return dict(book=book)

    @view_config(route_name='book-buy', renderer='json')
    def book_buy(self):

        id_ = int(self.request.matchdict.get('id'))

        if id_:

            book = self.hf.get_library_book_by_key(id_, self.session['loged_as'].get('email'))

            if not book:
                self.hf.add_library_book(int(self.request.matchdict.get('id')))
                return dict(status='ok')

            else:
                return dict(status='present')

        return dict(status='error')

    @view_config(route_name='library', renderer='json')
    def library(self):

        library= []

        for i in self.hf.get_library():

            library.append(
                {
                    'name': i.name,
                    'desc': i.description,
                    'author': i.author,
                    'image': i.image
                })

        return dict(library=library)

    @view_config(route_name='posts', renderer='json')
    def posts_for_user(self):
        return dict()

    @view_config(route_name='post_add', renderer='json')
    def add_post(self):
        j = self.request.json_body
        s = self.session

        some = datetime.now()

        a = j.get('content')
        b = s.get('loged_as').get('email')

        post = Post(a, b)
        self.DBSession.add(post)

        return dict()