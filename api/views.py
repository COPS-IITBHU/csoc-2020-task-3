from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer, TodoSerializer, CollaboratorSerializer, TodoUpateSerializer
from rest_framework import viewsets 
from .models import Todo
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework import mixins
from .permissions import IsOwnerOrCollaborator
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
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return Response({
                'id':instance.id,
                'title':instance.title,
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class TodoViewSet(mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrCollaborator)
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return TodoUpateSerializer
        return TodoSerializer
    def list(self, request, *args, **kwargs):
        queryset1 = Todo.objects.filter(creator=request.user)
        queryset2 = Todo.objects.filter(collaborators=request.user)
        queryset = (queryset1 | queryset2).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollaboratorViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = CollaboratorSerializer
    @action(methods=['put'], detail=True, permission_classes=[permissions.IsAuthenticated, ], url_path='add-collaborator', url_name='add_collaborator')
    def add_collaborator(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({'Error':'Invalid Todo Id'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.user == todo.creator:
                try:
                    collborators = request.data["collaborators"]
                except KeyError:
                    return Response({'Error':'Collaborator field not specified in request'}, status = status.HTTP_400_BAD_REQUEST)
                else:
                    collab_list = []
                    b=False
                    for collab in collborators:
                        try:
                            collab_name = collab['username']
                        except KeyError:
                            return Response({'Error':'No username provided'}, status = status.HTTP_400_BAD_REQUEST)
                        else:
                            try:
                                new_collab = User.objects.get(username=collab_name)
                            except User.DoesNotExist:
                                return Response({'Invalid username':collab_name}, status=status.HTTP_400_BAD_REQUEST)
                            if new_collab and new_collab != todo.creator:
                                collab_list.append(new_collab)
                            else:
                                b=True
                    todo.collaborators.add(*collab_list)
                    todo.save()
                    if b:
                        return Response({'Denied':'Creator can not be added as collaborator'}, status=status.HTTP_206_PARTIAL_CONTENT)
                    else:
                        return Response({'Success':'Added collaborators successfully'}, status=status.HTTP_200_OK)
                        
            else:
                raise PermissionDenied("You are not the creator of this Todo.")
    @action(methods=['patch'], detail=True, permission_classes=[permissions.IsAuthenticated, ], url_path='delete-collaborator', url_name='delete_collaborator')
    def delete_collaborator(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"Error":'Invalid Todo Id'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user == todo.creator:
            try:
                collborators = request.data["collaborators"]
            except KeyError:
                return Response({'Error':'Collaborator field not specified in request'}, status = status.HTTP_400_BAD_REQUEST)
            error_list = []
            collab_list = []
            collab_obj_list = todo.collaborators.all()
            for collab in collab_obj_list:
                collab_list.append(collab.username)
            for collab in collborators:
                try:
                    collab_name = collab['username']
                except KeyError:
                    return Response({'Error':'No username provided'}, status = status.HTTP_400_BAD_REQUEST)
                try:
                    collab_rem_obj = User.objects.get(username=collab_name)
                except User.DoesNotExist:
                    return Response({'Invalid username':collab_name}, status=status.HTTP_400_BAD_REQUEST) 
                if (collab_name in collab_list) and (collab_rem_obj):
                    todo.collaborators.remove(collab_rem_obj)
                    collab_list.remove(collab_name)
                    todo.save()
                else:
                    error_list.append(collab_name)
            if len(error_list):
                return Response({"Following name(s) were not collaborating to the task":error_list}, status = status.HTTP_206_PARTIAL_CONTENT)
            else:
                return Response({"success":'Removed all the specified collaborators'}, status=status.HTTP_204_NO_CONTENT)     
        else:
            raise PermissionDenied("You are not the creator of this Todo.")
        