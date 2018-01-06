def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('elixr-static', 'elixr2.web:static')
    config.add_route('home', '/')
