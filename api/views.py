from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .serializers import TodoCreateSerializer,TodoListSerializer,TodoDetailSerializer,AddCollaboraorSerializer
from .models import Todo,Collaborator
from django.db.models import CharField, Value

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
        todo=serializer.save()
        serializer = TodoCreateSerializer(todo)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

class TodoListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoListSerializer
    def get(self,request):
        user = request.user
        todos1 = Todo.objects.filter(creator=user)
        todos = Todo.objects.filter(collaborator__in=Collaborator.objects.filter(collaborator=user))
        todos1= todos1.annotate(user_type=Value('Creator',output_field=CharField()))
        todos = todos.annotate(user_type=Value('Collaborator',output_field=CharField()))
        todos=todos.union(todos1)
        serializer=TodoListSerializer(todos,many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK,safe=False)

class TodoDetailView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoDetailSerializer
    def put(self,request,id):
        try :
            todo = Todo.objects.get(id=id)
        except:
            error = {'message': "Todo doesn't exists!"}
            return Response(error, status=400)
        if request.user != Todo.objects.get(id=id).creator and Collaborator.objects.filter(todo=todo).filter(
                collaborator=request.user).count() == 0:
            error = {'message': "Unauthorized User"}
            return Response(error,status=401)
        data1 = { 'id': id , 'title':request.data['title']}
        serializer = self.get_serializer(data=data1)
        serializer.is_valid(raise_exception=True)
        todo = serializer.update(id)
        myserializer = TodoDetailSerializer(todo)
        return JsonResponse(myserializer.data, status=status.HTTP_200_OK, safe=False)

    def get(self,request,id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            error = {'message': "Todo doesn't exists!"}
            return Response(error, status=400)
        if request.user != Todo.objects.get(id=id).creator and Collaborator.objects.filter(todo=todo).filter(
                collaborator=request.user).count() == 0:
            error = {'message': "Unauthorized User"}
            return Response(error, status=401)
        id = id
        todo = Todo.objects.get(id=id)
        serializer = TodoDetailSerializer(todo)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def patch(self,request,id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            error = {'message': "Todo doesn't exists!"}
            return Response(error, status=400)
        if request.user != Todo.objects.get(id=id).creator and Collaborator.objects.filter(todo=todo).filter(
                collaborator=request.user).count() == 0:
            error = {'message': "Unauthorized User"}
            return Response(error, status=401)
        data = {'id': id, 'title': request.data['title']}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        todo=serializer.update(id)
        myserializer=TodoDetailSerializer(todo)
        return JsonResponse(myserializer.data, status=status.HTTP_200_OK,safe=False)

    def delete(self,request,id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            error = {'message': "Todo doesn't exists!"}
            return Response(error, status=400)
        if request.user != Todo.objects.get(id=id).creator and Collaborator.objects.filter(todo=todo).filter(
                collaborator=request.user).count() == 0:
            error = {'message': "Unauthorized User"}
            return Response(error, status=401)
        data = {'id': id}
        Todo.objects.get(id=id).delete()
        return Response(status=204)

class AddCollaborator(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddCollaboraorSerializer
    def post(self,request,id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            error = {'message': "Todo doesn't exists!"}
            return Response(error, status=400)
        if request.user != Todo.objects.get(id=id).creator :
            error = {'message': "Unauthorized User"}
            return Response(error,status=401)
        serializer = self.get_serializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        for list_elt in request.data:
            try:
                todo = Todo.objects.get(id=id)
            except:
                error = {'message': "Todo doesn't exists!"}
                return Response(error, status=400)
            try:
                user = User.objects.get(username=list_elt['collaborator_username'])
            except:
                error = {'message':list_elt['collaborator_username']+ " doesn't Exists!"}
                return Response(error,status=400)
            if request.user == User.objects.get(username=list_elt['collaborator_username']) :
                error = {'message': list_elt['collaborator_username']+ " is the creator itself,  Hence it can't be collaborated"}
                return Response(error, status=400)
            if Collaborator.objects.filter(collaborator=user, todo=todo).count() == 1:
                error = {'message': list_elt['collaborator_username']+" Already Collaborated"}
                return Response(error,status=400)
            Collaborator.objects.create(collaborator=user, todo=todo)
        return Response( status=200)


class RemoveCollaborator(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddCollaboraorSerializer
    def post(self,request,id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            error = {'message': "Todo doesn't exists!"}
            return Response(error, status=400)
        if request.user != Todo.objects.get(id=id).creator :
            error = {'message': "Unauthorized User"}
            return Response(error, status=401)
        serializer = self.get_serializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        for list_elt in request.data:
            try:
                todo = Todo.objects.get(id=id)
            except:
                error = {'message': "Todo doesn't exists!"}
                return Response(error,status=400)
            try:
                user = User.objects.get(username=list_elt['collaborator_username'])
            except:
                error = {'message': list_elt['collaborator_username']+" doesn't exists!"}
                return Response(error,status=400)
            try:
                instance = Collaborator.objects.get(collaborator=user, todo=todo)
                instance.delete()
            except:
                error = {'message': list_elt['collaborator_username']+" not Collaborated"}
                return Response(error,status=400)
        return Response( status=204)