from pyramid.events import subscriber, BeforeRender
from bookroom.lib import helpers as h

@subscriber(BeforeRender)
def add_before_render(event):
    request = event.get('request')

    event['session'] = request.session
    event['localizer'] = request.localizer

    event['h'] = h