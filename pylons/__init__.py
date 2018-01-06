import logging
from elixr2.web import Initializer as _Initializer

log = logging.getLogger(__name__)


class Initializer(_Initializer):
    """Application configuration and initialization.
    """

    def configure_user_services(self):
        """Plug in user services.
        """
        super(Initializer, self).configure_user_services()

        # configure utilities
        from elixr2.auth.interfaces import IAuthSchemas
        from .services.schemas import AuthSchemas

        reg = self.config.registry
        reg.registerUtility(AuthSchemas(), IAuthSchemas)
        x = reg.getUtility(IAuthSchemas)

    def configure_views(self):
        super(Initializer, self).configure_views()
        self.config.add_jinja2_search_path('pylons:templates', name='.html')
        self.config.include('pylons.routes')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    init =  Initializer(global_config, settings)
    init.configure_initializer()
    app = init.make_wsgi_app()
    return app
