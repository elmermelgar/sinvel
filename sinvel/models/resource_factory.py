from ziggurat_foundations.permissions import permission_to_pyramid_acls
from ziggurat_foundations.models.services.resource import ResourceService
from pyramid.security import Allow
from pyramid.security import Authenticated
from sinvel.models.models import Resource
from pyramid.httpexceptions import HTTPNotFound
class ResourceFactory(object):
    def __init__(self, request):

        self.__acl__ = [(Allow, Authenticated),u'view' ]
        if request.user:
            rid = request.matchdict.get("resource_id")

            if not rid:
                raise HTTPNotFound()
            self.resource = ResourceService.by_resource_id(rid,request.dbsession)
            if not self.resource:
                raise HTTPNotFound()
            if self.resource and request.user:
                # append basic resource acl that gives all permissions to owner

                self.__acl__ = self.resource.__acl__

                # append permissions that current user may have for this context resource
                permissions = self.resource.perms_for_user(request.user)
                print(permissions)
                for outcome, perm_user, perm_name in permission_to_pyramid_acls(permissions):
                    self.__acl__.append((outcome, perm_user, perm_name,))
                   # print(self.__acl__)