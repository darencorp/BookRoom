from pyramid.interfaces import IRoutesMapper


def get_routes(request):
    """Return all routes defined in the system
    """
    mapper = request.registry.queryUtility(IRoutesMapper)
    # prefix = request.registry.settings.get('prefix')
    return {r.name: r.pattern for r in mapper.get_routes()}
