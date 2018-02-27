import json

from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import func, desc, and_, or_
from bookroom.models.facades.home_facade import HomeFacade
from bookroom.models.Book import Book
from bookroom.models.BookRating import BookRating
from bookroom.models.ReviewRating import ReviewRating
from bookroom.models.User import User
from bookroom.models.Review import Review


class HomeView(object):
    def __init__(self, request):
        self.request = request
        self.DBSession = request.dbsession
        self.session = request.session
        self.settings = request.registry.settings

        self.hf = HomeFacade(request)

    @view_config(route_name='catalogue', renderer='../templates/views/catalogue.html')
    def catalogue(self):
        return dict()

    @view_config(route_name='get_catalogue', renderer='json')
    def get_catalogue(self):
        r = self.request

        s = r.session
        j = r.json_body

        catalogue_filter = j.get('filter', s.get('filter', None))
        s['filter'] = catalogue_filter

        if catalogue_filter:

            genres_filter = catalogue_filter.get('genres', None)
            genres = [x for x,y in genres_filter.items() if y]

            f_year = catalogue_filter.get('f_year', None)
            t_year = catalogue_filter.get('t_year', None)

            t_year_filter = (Book.year <= t_year) if t_year else True
            f_year_filter = (Book.year >= f_year) if f_year else True
            genre_filter = (Book.genre.in_(genres)) if genres else True

            book_query = self.DBSession.query(Book).filter(t_year_filter, f_year_filter, genre_filter).all()

        else:
            book_query = self.DBSession.query(Book).all()

        books = [
            {
                'id': i.id,
                'name': i.name,
                'author': i.author,
                'year': i.year,
                'genre': i.genre,
                'desc': i.description,
                'image': i.image
            } for i in book_query
        ]

        return dict(books=books, filter=catalogue_filter)

    @view_config(route_name='user', renderer='../templates/views/user-page.html')
    @view_config(route_name='user', xhr=True, renderer='json')
    def user(self):

        m = self.request.matchdict

        _id = m.get('id')

        try:
            id = int(_id)
        except ValueError:
            return HTTPNotFound()

        if not self.request.is_xhr:
            return dict(id=id)

        user_query = self.DBSession.query(User).filter(User.id == id).first()

        book_query = self.DBSession.query(BookRating, Book).join(User, User.id == id).join(Book,
                                                                                           BookRating.book_id == Book.id).filter(
            BookRating.user_id == User.email)

        book_reviews_query = self.DBSession.query(Review, Book).join(Book, Book.id == Review.book_id).join(User,
                                                                                                           User.email == Review.user_id).filter(
            User.id == id)

        user = {
            'first_name': user_query.first_name,
            'last_name': user_query.last_name,
            'image': user_query.avatar,
            'email': user_query.email
        }

        book_stared = [
            {
                'id': i.Book.id,
                'name': i.Book.name,
                'author': i.Book.author,
                'image': i.Book.image,
                'desc': i.Book.description,
                'rating': i.BookRating.value
            } for i in book_query
        ]

        book_reviews = dict()

        for i in book_reviews_query:
            if not book_reviews.get(i.Book.id):
                book_reviews[i.Book.id] = dict()

            if book_reviews[i.Book.id].get('reviews'):
                book_reviews[i.Book.id]['reviews'].append({
                    'body': i.Review.body,
                    'date': i.Review._date.strftime("%Y-%m-%d %H:%M")})
            else:
                book_reviews[i.Book.id]['reviews'] = [{
                    'body': i.Review.body,
                    'date': i.Review._date.strftime("%Y-%m-%d %H:%M")
                }]

            book_reviews[i.Book.id]['id'] = i.Book.id
            book_reviews[i.Book.id]['name'] = i.Book.name
            book_reviews[i.Book.id]['author'] = i.Book.author
            book_reviews[i.Book.id]['image'] = i.Book.image

        for k, v in book_reviews.items():
            v['reviews'].sort(key=lambda x: x['date'], reverse=True)

        return dict(user=user, book_stared=book_stared, book_reviews=book_reviews)

    @view_config(route_name='small_search', renderer='json')
    def small_search(self):
        j = self.request.json
        s = self.session

        c = j.get('criteria', s.get('search_criteria', ''))
        s['search_criteria'] = c

        book_query = self.DBSession.query(Book.id, Book.name, Book.image).filter(Book.name.like('%'+c+'%')).all()
        user_query = self.DBSession.query(User.id, User.first_name, User.last_name, User.avatar).filter(or_(User.first_name.like(c+'%'), User.last_name.like(c+'%'))).all()
        genre_query = self.DBSession.query(Book.genre).filter(Book.genre.like(c+'%')).distinct().all()

        book_data = [
            {
                'type': 'book',
                'id': i.id,
                'name': i.name,
                'image': i.image,
                'key': i.name
            } for i in book_query
        ]

        user_data = [
            {
                'type': 'user',
                'id': i.id,
                'first_name': i.first_name,
                'last_name': i.last_name,
                'avatar': i.avatar,
                'key': i.first_name
            } for i in user_query
        ]

        genre_data = [
            {
                'type': 'genre',
                'genre': i.genre,
                'key': i.genre
            } for i in genre_query
        ]

        result = book_data + user_data + genre_data

        sorted_results = sorted(result, key=lambda x: x['key'])

        if len(sorted_results) > 3:
            sorted_results = sorted_results[0:3]

        return sorted_results

    @view_config(route_name='global_search', renderer='../templates/views/search.html')
    @view_config(route_name='global_search', xhr=True, renderer='json')
    def global_search(self):
        p = self.request.params
        s = self.request.session

        is_genre = p.get('t')

        c = p.get('q', s.get('search_criteria', ''))
        s['search_criteria'] = c

        if not self.request.is_xhr:
            return dict(query=c, is_genre=is_genre)

        book_query = self.DBSession.query(Book.id, Book.name, Book.image).filter(Book.name.like('%' + c + '%')).all()
        user_query = self.DBSession.query(User.id, User.first_name, User.last_name, User.avatar).filter(
            or_(User.first_name.like(c + '%'), User.last_name.like(c + '%'))).all()

        genre_query = self.DBSession.query(Book.id, Book.name, Book.image).filter(Book.genre.like(c+'%')).all()

        book_data = [
            {
                'type': 'book',
                'id': i.id,
                'name': i.name,
                'image': i.image
            } for i in book_query
        ]

        user_data = [
            {
                'type': 'user',
                'id': i.id,
                'first_name': i.first_name,
                'last_name': i.last_name,
                'avatar': i.avatar
            } for i in user_query
        ]

        genre_data = [
            {
                'id': i.id,
                'name': i.name,
                'image': i.image
            } for i in genre_query
        ]

        result = book_data + user_data

        return dict(results=result, query=c, genre_results=genre_data)

    @view_config(route_name='get_book', renderer='../templates/views/book.html')
    @view_config(route_name='get_book', xhr=True, renderer='json')
    def get_book(self):

        r = self.request
        _id = r.matchdict.get('id')

        try:
            id = int(_id)
        except ValueError:
            return HTTPNotFound()

        if not self.request.is_xhr:
            book_id = self.DBSession.query(Book.id).filter(Book.id == id).first().id
            return dict(book_id=book_id)

        def get_user_review_rating(review_id):
            user_rating = self.DBSession.query(ReviewRating.value).filter(
                and_(ReviewRating.review_id == review_id, ReviewRating.user_id == r.authenticated_userid)).first()

            return user_rating.value if user_rating else None

        book_query = self.DBSession.query(Book).filter(Book.id == id).first()

        reviews_query = self.DBSession.query(
            Review, User,
            self.DBSession.query(func.count(ReviewRating.id)).filter(
                and_(ReviewRating.value == 1, ReviewRating.review_id == Review.id)).label('t_value'),
            self.DBSession.query(func.count(ReviewRating.id)).filter(
                and_(ReviewRating.value == -1, ReviewRating.review_id == Review.id)).label('f_value')) \
            .join(User,
                  User.email == Review.user_id).filter(
            Review.book_id == id).order_by(desc(Review._date)).all()

        rate_query = self.DBSession.query(func.avg(BookRating.value)).filter(BookRating.book_id == id).first()

        avg_rating = int(rate_query[0]) if rate_query[0] else 0

        u_rate = None

        reviews = [
            {
                'id': i.Review.id,
                'body': i.Review.body,
                'date': i.Review._date.strftime("%Y-%m-%d %H:%M"),
                'modified': i.Review.modified,
                'user_fname': i.User.first_name,
                'user_lname': i.User.last_name,
                'user_avatar': i.User.avatar,
                'user_id': i.User.id,
                'true_rating': i.t_value,
                'false_rating': i.f_value
            } for i in reviews_query
        ]

        if r.authenticated_userid:
            exist_rate = self.DBSession.query(BookRating).filter(
                and_(BookRating.user_id == r.authenticated_userid, BookRating.book_id == id)).first()

            if exist_rate:
                u_rate = exist_rate.value

            for i in reviews:
                i['user_vote'] = get_user_review_rating(i['id'])

        book = {
            'id': book_query.id,
            'name': book_query.name,
            'author': book_query.author,
            'year': book_query.year,
            'genre': book_query.genre,
            'desc': book_query.description,
            'image': book_query.image
        }

        user_rate = u_rate if u_rate else False

        return dict(book=book, reviews=reviews, user_rating=user_rate, avg_rating=avg_rating)
