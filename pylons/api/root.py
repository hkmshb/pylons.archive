import logging
from cornice.resource import resource
from elixr2.core import uuid_to_slug
from elixr2.auth.exceptions import AuthenticationError
from elixr2.auth.interfaces import ILoginService, IAuthSchemas
from .security import resolve_principals, RESTApiACL

log = logging.getLogger(__name__)



@resource(name='jwt_authorize', path='/jwt/authorize')
class JWTAuthorizeResource(object):

    def __init__(self, request, context=None):
        self.request = request

    def post(self):
        reg = self.request.registry
        schemas = reg.getUtility(IAuthSchemas)
        login_schema = schemas.login_schema(self.request)

        json_data = self.request.json_body.copy()
        data, errors = login_schema.load(json_data)
        if errors:
            log.debug('jwt login schema error: %s' % errors)
            return {'result': 'error: Invalid username and/or password'}

        username = json_data['email']
        password = json_data['password']
        try:
            lservice = reg.queryAdapter(self.request, ILoginService, name='api')
            user = lservice.login(username, password)

            # TODO: extend jwt token with extra claims
            return {
                'result': 'ok',
                'token': self.request.create_jwt_token(
                    str(user.uuid),
                    roles = resolve_principals(user)
                )
            }
        except AuthenticationError as ex:
            log.debug('jwt login error: %s' % str(ex))
            return {'result': 'error: Invalid username and/or password'}


@resource(name='api_root', path='/', factory=RESTApiACL, permission='authenticated')
class RootResource(object):
    """Discovers and returns a list of the root api endpoints for Pylons.
    """

    def __init__(self, request, context=None):
        self.request = request
        self.context = context

    def get(self):
        endpoints = {}
        app_url = self.request.application_url
        cornice_services = self.request.registry.cornice_services

        for path, service in cornice_services.items():
            name = service.name
            if name.startswith('collection'):
                name = name.replace('collection_', '')
                if name.startswith('_'):    # flag for collections to skip
                    continue
                endpoints[name] = "%s/%s" % (app_url, path)
        return endpoints
