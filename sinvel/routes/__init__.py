import os

def includeme(config):

    config.add_static_view(name='static', path='sinvel:static', cache_max_age=3600)
    #config.include('.routes')
    for module in os.listdir(os.path.dirname(__file__)):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        config.include('.'+module[:-3])
    del module
