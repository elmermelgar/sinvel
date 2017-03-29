def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    ############Seguridad################
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('user_register', '/user/register')
    config.add_route('user_create', '/user/create')
    ######################################
