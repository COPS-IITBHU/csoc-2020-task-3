from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import mixins
from django.core import serializers
from rest_framework.response import Response
from .serializers import TodoCreateSerializer,TodoListSerializer,TodoDetailSerializer,ColloboratorSerializer
from .models import Todo,Colloborator
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from django.contrib.auth.models import User



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
        todo=self.get_object(id)
        if not todo.creator==request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return self.retrieve(request,id)

    def put(self,request,id):
        todo=self.get_object(id)
        if not todo.creator==request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer=TodoDetailSerializer(todo,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id):
        todo=self.get_object(id)
        if not todo.creator==request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer=TodoDetailSerializer(todo,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        todo=self.get_object(id)
        if not todo.creator==request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ColloboratorAdd(generics.GenericAPIView,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    authentication_classes=[TokenAuthentication,]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ColloboratorSerializer
    lookup_field='id'
    
    def post(self,request,id=None):
        current_user=request.user
        datas=request.data
        print(datas)
        todo=Todo.objects.get(id=id)
        if not todo.creator==request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for data in datas:
            print(data)
            user=User.objects.get(username=data['username'])

            if user:
                c=Colloborator(owner=user,todo=todo)
                c.save()
            
        Collob=Colloborator.objects.filter(todo=todo)
        serializers=ColloboratorSerializer(Collob,many=True)
        return Response(serializers.data,status=status.HTTP_201_CREATED)

class ColloboratorRemove(generics.GenericAPIView,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    authentication_classes=[TokenAuthentication,]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ColloboratorSerializer
    lookup_field='id','coid'

    def get(self,request,id,coid):
        c=Colloborator.objects.get(id=coid)
        todo=Todo.objects.get(id=id)
        if not todo.creator==request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializers=ColloboratorSerializer(c)
        return Response(serializers.data)

    def delete(self,request,id,coid):
        current_user=request.user
        datas=request.data
        todo=Todo.objects.get(id=id)
        if not todo.creator==request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        c=Colloborator.objects.get(id=coid)
        print(c)
        c.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        

        







        
   


    