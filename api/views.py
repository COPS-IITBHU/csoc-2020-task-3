from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from django.contrib.auth import get_user_model

UserModel = get_user_model()


"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        """
        Creates a Todo entry for the logged in user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_queryset(self):
        user = self.request.user
        OwnTodo = Todo.objects.filter(creator=user.id)
        ContriTodo = contributor.objects.filter(
            user=user.id).values('todo')
        OthersTodo = Todo.objects.filter(pk__in=ContriTodo)
        return OwnTodo | OthersTodo


class TodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        OwnTodo = Todo.objects.filter(creator=user)
        ContriTodo = contributor.objects.filter(
            user=user).values('todo')
        OthersTodo = Todo.objects.filter(pk__in=ContriTodo)
        return OwnTodo | OthersTodo


class TodoCollab(generics.GenericAPIView):
    serializer_class = TodoContri
    permission_classes = (permissions.IsAuthenticated,)
    queryset = contributor

    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, creator=request.user)
        request.data['todo'] = todo.pk

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                UserModel, username=serializer.data['username'])
            contri = contributor.objects.get_or_create(todo=todo, user=user)

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoUnCollab(generics.GenericAPIView):
    serializer_class = TodoContri
    permission_classes = (permissions.IsAuthenticated,)
    queryset = contributor

    def delete(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, creator=request.user)
        request.data['todo'] = todo.pk

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                UserModel, username=serializer.data['username'])

            contri = get_object_or_404(
                contributor, user=user, todo=todo)
            contri.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
