def includeme(config):
    #config.add_static_view('static', 'static', cache_max_age=3600)
    #config.add_route('home', '/{resource_id}')
    config.add_route('home', '/')


    config.add_route('prueba', '/prueba')
    config.add_route('inicio', '/inicio')
    config.add_route('registrar_vehiculo','/RegistrarVehiculo')
    config.add_route('buscar_importacion','/RegistrarVehiculo/BuscarImportacion/{id_importacion}')
    config.add_route('guardar_registro_vehiculo','/RegistrarVehiculo/guardar')
    config.add_route('models','/models/{id_marca}/all_json_models')
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




    #################Salida Reparacion#############
    config.add_route('verificar_remolque', '/salida_reparacion/verificar_remolque')
    config.add_route('registro_control', '/salida_reparacion/registro_control')
    config.add_route('registro_control_guardar', '/salida_reparacion/registro_control/save')
    config.add_route('aprobar_salidas', '/salida_reparacion/aprobar_salidas')
    config.add_route('aprobar_salidas_guardar', '/salida_reparacion/aprobar_salidas/save')
    config.add_route('buscar_tipo_remolque', '/salida_reparacion/verificar_remolque/{id_tipo_remolque}')

    ################Entradas#######################
    config.add_route('registro_control_entrada','/entrada/registro_control_entrada')
    config.add_route('registro_entrada_control_guardar','/entrada/registro_entrada_control_guardar')

    config.add_route('remolques', '/get_remolques')