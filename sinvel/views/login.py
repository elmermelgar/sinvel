from pyramid.security import NO_PERMISSION_REQUIRED,Authenticated,DENY_ALL
from ziggurat_foundations.ext.pyramid.sign_in import ZigguratSignInSuccess
from ziggurat_foundations.ext.pyramid.sign_in import ZigguratSignInBadAuth
from ziggurat_foundations.ext.pyramid.sign_in import ZigguratSignOut
from ..models.models import Empleado,UsersGroup,User,Group
from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    view_config,
    view_defaults
    )


@view_config(context=ZigguratSignInSuccess, permission=NO_PERMISSION_REQUIRED)
def sign_in(request):

    user_id = request.context.user.id
    user_name=request.context.user.user_name
    query = request.dbsession.query(Empleado)
    query2 = request.dbsession.query(UsersGroup)
    #empleado = query.filter(Empleado.ID_USER == user_id).first()
    grupo = query2.filter(UsersGroup.user_id == user_id).first()
    name_group=grupo.group.group_name
    request.session['grupo'] = name_group
    print('Grupo de usuario:')
    print(request.session['grupo'] )
    #emp=request.session['empleado']
    #print(emp.NOMBRE)


    # actions performed on sucessful logon, flash message/new csrf token
    # user status validation etc.
    if request.context.came_from != '/':
        return HTTPFound(location=request.context.came_from,
                         headers=request.context.headers)
    else:
        return HTTPFound(location=request.route_url('home'),
                         headers=request.context.headers)


@view_config(context=ZigguratSignInBadAuth, permission=NO_PERMISSION_REQUIRED)
def bad_auth(request):
    # The user is here if they have failed login, this example
    # would return the user back to "/" (site root)
    return HTTPFound(location=request.route_url('login'),
                     headers=request.context.headers)
    # This view would return the user back to a custom view
    return HTTPFound(location=request.route_url('home'),
                     headers=request.context.headers)


@view_config(context=ZigguratSignOut, permission=NO_PERMISSION_REQUIRED)
def sign_out(request):
    return HTTPFound(location=request.route_url('login'),
                     headers=request.context.headers)
