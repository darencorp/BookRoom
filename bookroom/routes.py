def includeme(config):
    config.add_static_view('templates', 'templates/views/static', cache_max_age=3600)
    config.add_static_view('fonts', 'static/fonts', cache_max_age=3600)

    config.add_route('js', '/js')
    config.add_route('index', '/')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_route('logout', '/logout')

    config.add_route('catalogue', '/catalogue')
    config.add_route('get_catalogue', '/get_catalogue')
    config.add_route('user', '/user')
    config.add_route('small_search', '/front_search')
    config.add_route('global_search', '/search')
    config.add_route('get_book', '/book/{id}')

    config.add_route('image_upload', '/image_upload')
    config.add_route('add_book', '/add_book')
    config.add_route('add_review', '/add_review')
    config.add_route('update_reviews', '/update_reviews')
