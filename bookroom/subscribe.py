from pyramid.events import subscriber, BeforeRender
from bookroom.lib import helpers as h
from bookroom.lib.helpers import fix_webasset


@subscriber(BeforeRender)
def add_before_render(event):
    request = event.get('request')

    event['session'] = request.session
    event['base_path'] = fix_webasset(request.registry.settings.get('webassets.base_dir'))
    event['localizer'] = request.localizer

    event['h'] = h