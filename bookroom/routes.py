def includeme(config):
    config.add_route('js', '/js')
    config.add_route('index', '/')
    config.add_route('home', '/home')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_route('logout', '/logout')