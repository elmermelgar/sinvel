def includeme(config):
    #config.add_static_view('static', 'static', cache_max_age=3600)
    #config.add_route('home', '/{resource_id}')
    config.add_route('home', '/')


    config.add_route('prueba', '/prueba')
    config.add_route('inicio', '/inicio')
    config.add_route('registrar_vehiculo','/RegistrarVehiculo')
    config.add_route('buscar_importacion','/RegistrarVehiculo/BuscarImportacion/{id_importacion}')
    config.add_route('guardar_registro_vehiculo','/RegistrarVehiculo/guardar')
    #config.add_route('buscar_importacion', '/RegistrarVehiculo/BuscarImportacion?id_import={id_importacion}')
    #config.add_route('registrar_vehiculo', '/RegistroVehiculo/{id_importacion}')
    config.add_route('agregar_importador', '/AgregarImportador')
    config.add_route('guardar_importador', '/AgregarImportador/guardar')
    ##prueba para envio##


    ############Seguridad################
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('user_register', '/user/register')
    config.add_route('user_create', '/user/create')
    ######################################

    config.add_route('generar_reporte', '/generar')