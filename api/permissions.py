from rest_framework import permissions

class IsOwnerOrCollaborator(permissions.BasePermission):
    """
    custom permission to allow only creator and collaborator of a todo to view, edit and delete it. 
    """
    def has_object_permission(self, request, view, obj):
        return (obj.creator == request.user) or (request.user in obj.collaborators.all())