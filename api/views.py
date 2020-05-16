from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TodoCreateSerializer
from .serializers import TodoViewSerializer, CollaboratorSerializer
from .models import Todo
from django.http import Http404


class TodoListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = TodoViewSerializer

    def get(self, request):
        queryset = (Todo.objects.filter(
            creator=request.user) | Todo.objects.filter(collaborator=request.user)).distinct()
        response = self.get_serializer(queryset, many=True)
        print(response.data)
        return Response(response.data, status.HTTP_200_OK)


class CollaboratorAddView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollaboratorSerializer

    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except:
            raise Http404

    def post(self, request, pk):
        todo = self.get_object(pk)
        if (todo.creator == request.user):
            print(todo)
            serializer = self.get_serializer(data=request.data)
            serializer.add(pk)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class CollaboratorRemoveView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollaboratorSerializer

    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except:
            raise Http404

    def patch(self, request, pk):
        todo = self.get_object(pk)

        if todo.creator == request.user:
            serializer = self.get_serializer(data=request.data)
            serializer.remove(pk)
            return(Response(status=status.HTTP_200_OK))
        else:
            return(Response(status=status.HTTP_403_FORBIDDEN))


class TodoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            todo = Todo.objects.filter(pk=pk, creator=self.request.user) | Todo.objects.filter(
                pk=pk, collaborator=self.request.user)
            print(todo[0])
            return todo[0]
        except:
            raise Http404

    def get(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoViewSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoViewSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoViewSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoCreateView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
