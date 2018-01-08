from elixr2.auth.interfaces import ILoginService
from elixr2.ctx.interfaces import IDbContext
from .services import APILoginService



def includeme(config):
    # register services
    reg = config.registry
    reg.registerAdapter(factory=APILoginService, required=(IDbContext,),
                        provided=ILoginService, name='api')

    # make cornice & api configs
    config.route_prefix = 'api/v1'
    config.include('pyramid_jwt')
    config.include('cornice')
    config.scan('.root')
