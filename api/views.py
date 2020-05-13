from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import mixins
from django.core import serializers
from rest_framework.response import Response
from .serializers import TodoCreateSerializer,TodoListSerializer,TodoDetailSerializer
from .models import Todo
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication



"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoCreateView(generics.GenericAPIView,mixins.CreateModelMixin):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    authentication_classes=[TokenAuthentication,]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer
    


    def post(self, request):
        data=request.data
        current_user=request.user
        print(data,current_user)
        a=Todo.objects.create(title=data['title'],creator=current_user)
        a.save()
        serializer=TodoCreateSerializer(a)

        return Response(serializer.data,status=status.HTTP_201_CREATED)


class TodoListView(generics.GenericAPIView,mixins.ListModelMixin):
    authentication_classes=[TokenAuthentication,]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoListSerializer

    def get(self,request):
        current_user=request.user
        print('user',current_user)
        todo=Todo.objects.filter(creator=current_user)
        serializers=TodoListSerializer(todo,many=True)
        return Response(serializers.data)


class TodoDetailView(generics.GenericAPIView,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    authentication_classes=[TokenAuthentication,]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoListSerializer
    lookup_field='id'
    queryset=Todo.objects.all()
    def get_object(self,id):
        try:
            todo=Todo.objects.get(id=id)
            return todo

        except todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        return self.retrieve(request,id)

    def put(self,request,id):
        todo=self.get_object(id)
        serializer=TodoDetailSerializer(todo,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id):
        todo=self.get_object(id)
        serializer=TodoDetailSerializer(todo,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        todo=self.get_object(id)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

   


    