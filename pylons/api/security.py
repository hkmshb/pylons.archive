from zope.interface import implementer
from pyramid.security import ALL_PERMISSIONS, Allow, Authenticated, Deny, Everyone
from elixr2.web.interfaces import IACLResource

import logging
log = logging.getLogger(__name__)


@implementer(IACLResource)
class RESTApiACL(object):
    __acl__ = [
        (Allow, Authenticated, 'authenticated'),
        (Deny, Everyone, ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request


def resolve_principals(user):
    """Get and return the API specific roles that are applicable for the
    provided user.
    """
    assert user, "Expected a User model instance."
    # default principal included for all authenticated users
    principals = [Authenticated]
    # other principals build from api specific roles
    principals += ['role:%s' % r
                   for r in user.roles
                   if r.name.startswith('api')
                   ]
    return principals


def jwt_principals_finder(userid, request):
    """Retrieves the principals included in a JWT claims data.
    """
    principals = request.jwt_claims.get('roles', [])
    return principals
