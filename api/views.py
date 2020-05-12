from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import Todo


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
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class TodoGetView(generics.GenericAPIView):
    
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoGetSerializer

    def get(self, request):
        user = request.user
        data = Todo.objects.all().filter(creator=user)
        serializer = self.get_serializer(data, many=True)
        print("\n\n\nDATA:::   ", serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TodoDetailView(generics.GenericAPIView):
    
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoDetailSerializer

    def get(self, request, id):
        print('\n\n\n\n', id)
        todo = Todo.objects.filter(creator = request.user, id= id).first()
        print('\n\n\n\n', todo)
        serializer = self.get_serializer(todo)
        return Response(serializer.data,status=status.HTTP_200_OK, headers=None)


    def put(self, request, id):
        todo = Todo.objects.filter(creator = request.user, id= id).first()
        serializer = self.get_serializer(todo)
        s= serializer.put(request.data['title'])
        return  Response( s,status=status.HTTP_200_OK, headers=None)
        
    def patch(self, request, id):
        todo = Todo.objects.filter(creator = request.user, id= id).first()
        serializer = self.get_serializer(todo)
        s = serializer.put(request.data['title'])
        return Response( s,status=status.HTTP_200_OK, headers=None)

    def delete(self, request, id):
        todo = Todo.objects.filter(creator = request.user, id= id).first()
        serializer = self.get_serializer(todo)
        serializer.delete()
        print('\n\n\n--------------DELETED -----------------')
        return Response(status=status.HTTP_204_NO_CONTENT)
