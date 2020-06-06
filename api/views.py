from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer,TodoSerializer
from .models import Todo
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
        return Response(serializer.data, status=status.HTTP_200_OK)

class TodoGetView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer
    queryset=Todo.objects.all()
    def get(self,request):
        queryset = Todo.objects.filter(collaborator__exact=request.user)
        serializer = TodoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TodoDetailView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer
    def get(self,request,id):
        query = Todo.objects.get(id=id,collaborator=request.user)
        serializer = TodoSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self,request,id):
        query = Todo.objects.get(id=id,collaborator=request.user)
        serializers=TodoSerializer(query,data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,id):
        query = Todo.objects.get(id=id,collaborator=request.user)
        serializers=TodoSerializer(query,data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        query = Todo.objects.get(id=id,collaborator=request.user)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TodoAddCollaborator(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer
    def post(self,request,id):
        try:
            query = Todo.objects.get(id=id,creator=request.user)
        except:
            return Response({"message":"You are not creator"},status=status.HTTP_204_NO_CONTENT)
        user=User.objects.get(username=request.data['username'])
        query.collaborator.add(user)
        return Response(status=status.HTTP_200_OK)

class TodoRemoveCollaborator(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer
    def post(self,request,id):
        try:
            query = Todo.objects.get(id=id,creator=request.user)
        except:
            return Response({"message":"You are not creator of this collaborator"},status=status.HTTP_204_NO_CONTENT)
        user=User.objects.get(username=request.data['username'])
        query.collaborator.remove(user)            
        return Response(status=status.HTTP_200_OK)