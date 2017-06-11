from ziggurat_foundations.permissions import permission_to_pyramid_acls
from pyramid.security import Allow
from pyramid.security import Authenticated
class RootFactory(object):
    def __init__(self, request):
        self.__acl__ = [(Allow, Authenticated,u'view'), (Allow, Authenticated, u'admin'),]
        # general page factory - append custom non resource permissions
        # request.user object from cookbook recipie
        if request.user:
            # for most trivial implementation

            # for perm in request.user.permissions:
            #     self.__acl__.append((Allow, perm.user.id, perm.perm_name,))

            # or alternatively a better way that handles both user
            # and group inherited permissions via `permission_to_pyramid_acls`

            for outcome, perm_user, perm_name in permission_to_pyramid_acls(
                  request.user.permissions):
                print( request.user.permissions)
                self.__acl__.append((outcome, perm_user, perm_name))