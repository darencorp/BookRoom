def includeme(config):
    config.add_static_view('templates', 'templates/views/static', cache_max_age=3600)

    config.add_route('js', '/js')
    config.add_route('index', '/')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_route('logout', '/logout')

    config.add_route('catalogue', '/catalogue')
    config.add_route('get_catalogue', '/get_catalogue')
    config.add_route('user', '/user/{id}')
    config.add_route('small_search', '/front_search')
    config.add_route('global_search', '/search')
    config.add_route('get_book', '/book/{id}')

    config.add_route('image_upload', '/image_upload')
    config.add_route('add_book', '/add_book')
    config.add_route('update_book', '/update_book')
    config.add_route('delete_book', '/delete_book')
    config.add_route('add_review', '/add_review')
    config.add_route('update_reviews', '/update_reviews')
    config.add_route('vote_book', '/vote_book')
    config.add_route('vote_review', '/vote_review')

    config.add_route('avatar_change', '/avatar_change')
    config.add_route('change_data', '/change_data')
    config.add_route('change_password', '/change_password')
