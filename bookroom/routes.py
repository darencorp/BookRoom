def includeme(config):
    # config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('js', '/js')
    config.add_route('index', '/')
    config.add_route('home', '/home')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_route('logout', '/logout')
    config.add_route('upload', '/upload')

    config.add_route('book', '/book/{id}')
    config.add_route('book-buy', '/book-process/{id}')

    config.add_route('library', 'library')

    config.add_route('posts', 'posts/{user}')
    config.add_route('post_add', 'post/new')
    config.add_route('post_delete', 'posts/{id}')
