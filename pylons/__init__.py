from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.add_jinja2_search_path('pylons:templates', name='.html')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
