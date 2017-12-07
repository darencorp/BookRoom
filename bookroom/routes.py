def includeme(config):
    config.add_static_view('templates', 'templates/views/static', cache_max_age=3600)
    config.add_static_view('fonts', 'static/fonts', cache_max_age=3600)

    config.add_route('js', '/js')
    config.add_route('index', '/')
    config.add_route('home', '/home')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_route('logout', '/logout')

    config.add_route('get_book', '/book')
