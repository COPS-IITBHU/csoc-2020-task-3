from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from .serializers import *
from .models import Todo
from django.contrib.auth.models import User


"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

class TodoAddCollaboratorsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCollaboratorsSerializer

    def post(self, request, id):
        """
        request body should contain field named "usernames",
        which contains single or comma seperated usernames that are
        to be used as collaborators.
        """
        serializer = TodoCollaboratorsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):     
            usernames = request.data['usernames'].replace(' ','').split(',')
            usernames = set(usernames)
            usernames = list(usernames)
            try:
                todo = Todo.objects.get(id=id)
            except:
                return Response({ "todo": "Not found" }, status=404)
            if request.user == todo.creator:
                all_users = []
                for user in User.objects.all():
                    all_users.append(user.username)
                response = {
                    "success": [],
                    "alreadyCollaborator": [],
                    "invalidUsername":[]
                }
                for user in usernames:
                    if user in todo.collaborators:
                        response['alreadyCollaborator'].append(user)
                    elif user not in all_users:
                        response['invalidUsername'].append(user)
                    else:
                        response['success'].append(user)
                        todo.collaborators.append(user)
                        todo.save()
                if not response['success']:
                    del response['success']
                if not response['alreadyCollaborator']:
                    del response['alreadyCollaborator']
                if not response['invalidUsername']:
                    del response['invalidUsername']
                return Response(response, status=200)
            else:
                return Response({ "todo": "Not found" }, status=404)

class TodoRemoveCollaboratorsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCollaboratorsSerializer
    
    def post(self, request, id):
        """
        request body should contain field named "usernames",
        which contains single or comma seperated usernames that are
        to be used as collaborators.
        """
        serializer = TodoCollaboratorsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):     
            usernames = request.data['usernames'].replace(' ','').split(',')
            usernames = set(usernames)
            usernames = list(usernames)
            try:
                todo = Todo.objects.get(id=id)
            except:
                return Response({ "todo": "Not found" }, status=404)
            if request.user == todo.creator:
                all_users = []
                for user in User.objects.all():
                    all_users.append(user.username)
                response = {
                    "success": [],
                    "invalidUsername":[]
                }
                for user in usernames:
                    if user in todo.collaborators:
                        response['success'].append(user)
                        todo.collaborators.remove(user)
                        todo.save()
                    else:
                        response['invalidUsername'].append(user)
                if not response['success']:
                    del response['success']
                if not response['invalidUsername']:
                    del response['invalidUsername']
                return Response(response, status=200)
            else:
                return Response({ "todo": "Not found" }, status=404)

class TodoView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer

    def get(self, request, id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            return Response({ "todo": "Not found" }, status=404)
        if request.user == todo.creator or str(request.user) in todo.collaborators:
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=200)
        else:
            return Response({"todo": "Not found" }, status=404)
    
    def put(self, request, id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            return Response({ "todo": "Not found" }, status=404)
        if request.user == todo.creator or str(request.user) in todo.collaborators:
            serializer = TodoSerializer(todo ,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"todo": "Not found" }, status=404)
    
    def patch(self, request, id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            return Response({ "todo": "Not found" }, status=404)
        if request.user == todo.creator or str(request.user) in todo.collaborators:
            serializer = TodoSerializer(todo ,data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"todo": "Not found" }, status=404)
    
    def delete(self, request, id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            return Response({ "todo": "Not found" }, status=404)
        if request.user == todo.creator or str(request.user) in todo.collaborators:
            todo.delete()
            return Response({ "todo": "Delete successfull" }, status=200)
        else:
            return Response({"todo": "Not found" }, status=404)

class TodoListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoListSerializer
    queryset = Todo.objects.all()

    def get(self, request):
        todos_self = Todo.objects.filter(creator__exact=request.user)
        serializers_self = TodoListSerializer(todos_self, many=True)
        todos_other = Todo.objects.filter(collaborators__contains=request.user)
        serializers_other = TodoListSerializer(todos_other, many=True)
        return Response({
            "createdTODOs": serializers_self.data,
            "collaboratedTODOs": serializers_other.data
        }, status=200)

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
        return Response(serializer.save(), status=200)
