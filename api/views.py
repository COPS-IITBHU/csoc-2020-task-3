from rest_framework import generics
from rest_framework import permissions
from rest_framework import status,exceptions
from rest_framework.response import Response
from .serializers import *
from .models import Todo
from rest_framework import mixins
from django.contrib.auth.models import User


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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class TodoListView(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TodoListSerializer
    def get_queryset(self):       
        user=self.request.user
        obj=Todo.objects.filter(creator=user)
        obj1=Todo.objects.filter(collab=user)
        f_list=[]
        for x in obj:
            f_list.append(x)
        for x in obj1:
            f_list.append(x)
        
        return f_list

class TodoOpsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TodoOpsSerializer
    def get_queryset(self,id=None):
        user=self.request.user
        obj=Todo.objects.filter(creator=user)
        obj1=Todo.objects.filter(collab=user)
        obj2= obj | obj1
        return obj2

class UserList(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer


class CollaboratorAddView(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CollabSerializer

    def post(self,request,pk):
        user=User.objects.get(username=request.data['username'])
        todo=Todo.objects.get(pk=pk)
        if self.request.user==todo.creator:
            todo.collab.add(user)
            print(todo.collab.all())
            return Response( status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    
class CollaboratorRemoveView(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CollabSerializer

    def post(self,request,pk):
        
        user=User.objects.get(username=request.data['username'])
        todo=Todo.objects.get(pk=pk)
        if self.request.user == todo.creator:
            if user in todo.collab.all():
                todo.collab.remove(user)
                print( todo.collab.all())
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    