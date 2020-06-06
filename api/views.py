from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer, TodoSerializer, CollaboratorSerializer
from .models import Todo
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class TodoCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data=serializer.data
        return Response(data,status=status.HTTP_200_OK)

class ListTodo(generics.GenericAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self,request):
        todo=Todo.objects.filter(creator=request.user)
        todo2=Todo.objects.filter(collaborators=request.user)
        serializer=TodoSerializer(todo, many=True)
        serializer2=TodoSerializer(todo2, many=True)
        return Response({'officialTodo':serializer.data, 
                        'collTodo':serializer2.data}, status=status.HTTP_200_OK)

class DetailTodo(generics.GenericAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def  get(self,request,id):
        todo=get_object_or_404(Todo, id=id)
        if request.user==todo.creator or str(request.user) in todo.collaborators:
            serializer=TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        todo=get_object_or_404(Todo, id=id)
        if request.user==todo.creator or str(request.user) in todo.collaborators:
            todo.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self,request,id):
        todo=get_object_or_404(Todo, id=id)
        if request.user==todo.creator or str(request.user) in todo.collaborators:
            serializer=TodoSerializer(todo, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,id):
        todo=get_object_or_404(Todo, id=id)
        if request.user==todo.creator or str(request.user) in todo.collaborators:
            serializer=TodoSerializer(todo, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class TodoAddCollaborator(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = CollaboratorSerializer
    def post(self,request,id):
        todo=get_object_or_404(Todo, id=id)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if todo.creator==request.user:
                data=serializer.validated_data
                user=get_object_or_404(User, username=data['username'])
                todo.collaborators.add(user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'Error':"Invalid Input"}, status=status.HTTP_404_NOT_FOUND)

class TodoRemoveCollaborator(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorSerializer
    def post(self,request,id):
        todo=get_object_or_404(Todo, id=id)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if todo.creator==request.user:
                data=serializer.validated_data
                user=get_object_or_404(User, username=data['username'])
                todo.collaborators.remove(user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'Error':"Invalid Input"}, status=status.HTTP_404_NOT_FOUND)