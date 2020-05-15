from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer, TodoSerializer
from .models import Todo
from django.shortcuts import get_object_or_404


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
        todoData = serializer.data
        return Response(todoData, status=status.HTTP_200_OK)


class TodoGetView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def get(self, request):
        user = request.user
        todos = Todo.objects.filter(creator=user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TodoDetailView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer

    def get(self, request, id):
        todo = get_object_or_404(Todo, id=id, creator=request.user)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        todo = get_object_or_404(Todo, id=id, creator=request.user)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        todo = get_object_or_404(Todo, id=id, creator=request.user)
        todo.title = request.data['title']
        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        todo = get_object_or_404(Todo, id=id, creator=request.user)
        if request.data['title']:
            todo.title = request.data['title']
        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
