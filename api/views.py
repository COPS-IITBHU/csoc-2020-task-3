from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer, TodoSerializer, TodoCollaboratorSerializer
from .models import Todo

class IsOwnerOrCollaborator(permissions.BasePermission):
    def has_object_permission(self, request, View, obj):
        return request.user == obj.creator or obj.collaborators == request.user

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, View, obj):
        return request.user == obj.creator

"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoCreateView(generics.GenericAPIView):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        """
        Creates a Todo entry for the logged in user.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else :
            return Response(status=serializer.errors)

class TodoView(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrCollaborator)
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

class TodoListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        ownerqueryset = Todo.objects.filter(creator=request.user)
        collabqueryset = Todo.objects.filter(collaborators=request.user)
        ownerserializer = TodoSerializer(ownerqueryset, many=True)
        collabserializer = TodoSerializer(collabqueryset, many=True)
        return Response({
            'owner':ownerserializer.data,
            'collaborator':collabserializer.data,
        })


'''
for adding or removing collaborators
request (PUT or PATCH) format

{
    "usernames": <Array of usernames to be added or removed>
}
'''

class TodoAddCollaboratorView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = TodoCollaboratorSerializer
    queryset = Todo.objects.all()
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['add'] = True
        return context


class TodoRemoveCollaboratorView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = TodoCollaboratorSerializer
    queryset = Todo.objects.all()
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['add'] = False
        return context

