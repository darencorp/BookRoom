from pyramid import renderers
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from webassets import Bundle

from bookroom.lib.security import groupfinder, Root


def include_js(config):
    minjs = Bundle(
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/uikit/dist/js/uikit.min.js',
        'node_modules/uikit/dist/js/uikit-icons.min.js',
        'node_modules/angular/angular.min.js',
        'node_modules/angular-ui-router/release/angular-ui-router.min.js',

        'js/lib/jquery.nano.js',

        'js/app.js',

        'js/controllers/login.ctrl.js',
        'js/controllers/home.ctrl.js',
        'js/controllers/catalogue.ctrl.js',
        'js/controllers/user_page.ctrl.js',
        'js/controllers/search.ctrl.js',

        'js/services/home.service.js',

        output='js/generated.js',
        filters='jsmin'
    )
    config.add_webasset('minjs', minjs)


def include_css(config):
    mincss = Bundle(

        'node_modules/uikit/dist/css/uikit.css',

        'css/app.css',
        'css/home.css',

        output='css/generated.css',
        filters='cssmin'
    )
    config.add_webasset('mincss', mincss)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.set_session_factory(SignedCookieSessionFactory('secret', max_age=1200))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_authentication_policy(SessionAuthenticationPolicy('secret', callback=groupfinder))
    config.set_root_factory(Root)

    config.add_mako_renderer('.html')
    json_renderer = renderers.JSON()
    config.add_renderer('json', json_renderer)

    config.include('.models')
    config.include('.routes')
    config.include(include_js)
    config.include(include_css)
    config.scan()
    return config.make_wsgi_app()
