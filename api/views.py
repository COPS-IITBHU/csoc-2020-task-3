from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer
from .serializers import TodoListViewSerializer
from .models import Todo


"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = TodoListViewSerializer

    def get(self, request):
        queryset = Todo.objects.filter(creator=request.user)
        response = self.get_serializer(queryset, many=True)
        return Response(response.data, status.HTTP_200_OK)


class TodoCreateView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
