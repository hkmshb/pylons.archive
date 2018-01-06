from pyramid.view import view_config



@view_config(route_name='home', renderer='index.html')
def index(request):
    return {}
