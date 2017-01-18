from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from webassets import Bundle


def include_js(config):
    minjs = Bundle(
        'js/app.js',

        output='js/generated.js',
        filters='jsmin'
    )

    config.add_webasset('minjs', minjs)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.set_session_factory(SignedCookieSessionFactory('itsaseekreet'))

    config.add_mako_renderer('.html')

    config.include('.models')
    config.include('.routes')
    config.include(include_js)
    config.scan()
    return config.make_wsgi_app()
