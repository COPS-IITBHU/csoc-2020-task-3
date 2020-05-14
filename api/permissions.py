from rest_framework.permissions import BasePermission
from .models import Todo


class OnlyCreator(BasePermission):
    message = "This can only done by Creator Or Please check your id"
    
    def has_permission(self, request, view):
        id = view.kwargs['id']
        todo = Todo.objects.filter(id = id)
        if todo:
            if request.user == todo[0].creator:
                return True
        return False


class CollaboratorAndCreator(BasePermission):
    message = "This can be done by Only Collaborator and Creator"

    def has_object_permission(self, request, view, object):
        todo = Todo.objects.filter(id = object.id)
        if todo:
            if request.user == todo[0].creator or request.user in todo[0].Collaborators.all():
                return True
        return False



