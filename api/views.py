from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer, TodoSerializer, AddCollaboratorSerializer, RemoveCollaboratorSerializer
from .models import Todo
from .permissions import OnlyCreator, CollaboratorAndCreator
from itertools import chain
"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""
class TodoallgetView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, CollaboratorAndCreator,)
    serializer_class = TodoSerializer

    def get_queryset(self):
        todocreator = Todo.objects.filter(creator = self.request.user)
        for todo in todocreator:
            todo.iscreator = True
            todo.iscollaborator = False
            todo.save()

        todocollaborator = Todo.objects.filter(Collaborators = self.request.user)
        for todo in todocollaborator:
            todo.iscreator = False
            todo.iscollaborator = True
            todo.save()
    
        return chain(todocreator, todocollaborator)


class TodoIdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, CollaboratorAndCreator,)
    serializer_class = TodoSerializer
    lookup_field = 'id'
    queryset = Todo.objects.all()

    def get_queryset(self, **kwargs):
        todocreator = Todo.objects.filter(creator = self.request.user, id = self.kwargs['id'])
        if todocreator:
            todocreator[0].iscreator = True
            todocreator[0].iscollaborator = False
            todocreator[0].save()

        todocollaborator = Todo.objects.filter(Collaborators = self.request.user, id = self.kwargs['id'])
        if todocollaborator:
            todocollaborator[0].iscreator = False
            todocollaborator[0].iscollaborator = True
            todocollaborator[0].save()
    
        return todocreator | todocollaborator
    


class TodoCreateView(generics.GenericAPIView):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoCreateSerializer

    def post(self, request):
        """
        Creates a Todo entry for the logged in user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        response = {
            'id': data.id,
            'title': data.title
        }
        return Response(response, status=status.HTTP_200_OK)

class AddCollaboratorView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, OnlyCreator,)
    serializer_class = AddCollaboratorSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.add_collaborators(self.kwargs['id'], request.user)
            return Response({'message': 'Success'}, status = status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Failure'}, status = status.HTTP_404_NOT_FOUND) 


class RemoveCollaboratorView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, OnlyCreator,)
    serializer_class = RemoveCollaboratorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.remove_collaborators(self.kwargs['id'])
            return Response({'message': 'Success'}, status = status.HTTP_200_OK)
        else:
            return Response({'message': 'Failure'}, status = status.HTTP_404_NOT_FOUND) 