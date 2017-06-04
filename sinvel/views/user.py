

from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    view_config,
    view_defaults
    )
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError
from ..models import seguridad
import bcrypt
import transaction

view_defaults(route_name='login')
class UserView(object):
    def __init__(self, request):
        self.request = request
        self.item = seguridad.User()

    @view_config(route_name='login', request_method='GET', renderer='../templates/login.jinja2')
    def registerUser(self):
        user=seguridad.User()
        return {'user': user}

    @view_config(route_name='user_create', request_method='POST')
    def createUser(self):
        try:
            data = self.request.POST
            user = seguridad.User()
            for key, value in data.items():
                if(key=='user_password'):

                    hashed =bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
                    print(hashed)
                    if bcrypt.hashpw(value.encode('utf-8'), hashed) == hashed:
                        print("It Matches!")
                    else:
                        print("It Does not Match :(")
                    setattr(user, key, hashed)

                else:
                    setattr(user, key, value)
            self.request.dbsession.add(user)

            transaction.commit()
        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
        return HTTPFound(location='/')





db_err_msg = """\
    Pyramid is having a problem using your SQL database.  The problem
    might be caused by one of the following things:

    1.  You may need to run the "initialize_myproj_db" script
        to initialize your database tables.  Check your virtual
        environment's "bin" directory for this script and try to run it.

    2.  Your database server may not be running.  Check that the
        database server referred to by the "sqlalchemy.url" setting in
        your "development.ini" file is running.

    After you fix the problem, please restart the Pyramid application to
    try it again.
    """