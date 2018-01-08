import logging
from elixr2.web import Initializer as _Initializer

log = logging.getLogger(__name__)


class Initializer(_Initializer):
    """Application configuration and initialization.
    """

    def configure_authentication(self):
        """Set up authentication and authorization policies.
        """
        import pyramid.tweens
        from pyramid.authorization import ACLAuthorizationPolicy
        from pyramid.authentication import SessionAuthenticationPolicy
        from pyramid_jwt import create_jwt_authentication_policy
        from pyramid_multiauth import MultiAuthenticationPolicy
        from elixr2.web.auth.principals import (
            resolve_principals as get_principals,
            get_request_user
            )
        from .api.security import jwt_principals_finder

        authz_policy = ACLAuthorizationPolicy()
        ses_authn_policy = SessionAuthenticationPolicy(callback=get_principals)
        jwt_authn_policy = create_jwt_authentication_policy(self.config,
            callback=jwt_principals_finder)

        multi_auth_args = [jwt_authn_policy, ses_authn_policy]
        authn_policy = MultiAuthenticationPolicy(multi_auth_args)

        self.config.set_authentication_policy(authn_policy)
        self.config.set_authorization_policy(authz_policy)

        # We need to carefully be above TM view, but below exc view so that
        # internal server error page doesn't trigger session authentication
        # that accesses the database
        self.config.add_tween(
            "elixr2.web.auth.tweens.SessionInvalidationTweenFactory",
            under="pyramid_tm.tm_tween_factory")

        # # TODO: Grab incoming auth details changed events
        # from websauna.system.auth import subscribers
        # self.config.scan(subscribers)

        # Experimental support for transaction aware properties
        try:
            from pyramid_tm.reify import transaction_aware_reify
            self.config.add_request_method(
                callable=transaction_aware_reify(self.config, get_request_user),
                name="user", property=True, reify=False)
        except ImportError:
            self.config.add_request_method(get_request_user, 'user', reify=True)

        ## request method for jwt
        def create_jwt_token(request, principal, expiration=None, **claims):
            return jwt_authn_policy.create_token(principal, expiration, **claims)

        def jwt_claims(request):
            return jwt_authn_policy.get_claims(request)

        self.config.add_request_method(create_jwt_token, 'create_jwt_token')
        self.config.add_request_method(jwt_claims, 'jwt_claims', reify=True)

    def configure_user_services(self):
        """Plug in user services.
        """
        super(Initializer, self).configure_user_services()

        # configure utilities
        from elixr2.auth.interfaces import IAuthSchemas
        from .services.schemas import AuthSchemas

        reg = self.config.registry
        reg.registerUtility(AuthSchemas(), IAuthSchemas)

    def configure_views(self):
        super(Initializer, self).configure_views()
        self.config.add_jinja2_search_path('pylons:templates', name='.html')
        self.config.include('pylons.routes')

    def configure_initializer(self):
        super(Initializer, self).configure_initializer()

        # include api configurations
        self.config.include('pylons.api')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    init = Initializer(global_config, settings)
    init.configure_initializer()
    app = init.make_wsgi_app()
    return app
