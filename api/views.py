from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import Todo

class TodoGetView(generics.GenericAPIView):
    
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoGetSerializer

    def get(self, request):
        '''
        Responds with Todos associated with the logged in user
        '''
        user = request.user
        data = Todo.objects.all().filter(creator=user)
        serializer = self.get_serializer(data, many=True)
        colab = data = Todo.objects.all().filter(collaborator=user)
        serializer2 = self.get_serializer(colab, many=True)
        # The list contain two dicts 
        # One for created todos and second for collaborated todos
        output = [serializer.data, serializer2.data]
        return Response(output ,status=status.HTTP_200_OK)

class TodoCreateView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        """
        Creates a Todo entry for the logged in user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = serializer.save()
        # If collaborators are given, add them
        if 'collaborators' in request.data.keys():
            serializer.addCollaborators(id,request.data['collaborators'])
        # Take the data from serializer and add the id to it
        output = dict(serializer.data)
        output['id'] = id
        return Response(output,status=status.HTTP_201_CREATED)

class TodoRemoveCollaboratorView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorSerializer

    def patch(self, request, id):
        # ONLY FOR CREATORS
        try:
            todo = Todo.objects.get(id= id)
        except Todo.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

        todo = Todo.objects.get(id= id)
        if (todo.creator != request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        s = self.get_serializer(request.data)
        s.remover(id)
        return Response(status = status.HTTP_200_OK)

class TodoAddCollaboratorView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorSerializer
    
    def post(self, request, id):
        # ONLY FOR CREATORS
        try:
            todo = Todo.objects.get(id= id)
        except Todo.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

        todo = Todo.objects.get(id= id)
        if (todo.creator != request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)

        s = self.get_serializer(request.data)
        s.adder(id)
        return Response(status = status.HTTP_200_OK)

class TodoDetailView(generics.GenericAPIView):
    
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = Todoializer

    def get(self, request, id):
        try:
            todo = Todo.objects.get(id= id)
        except Todo.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
        # Each Todo is accessible only to its creator and collaborators
        check = False # To check if the user has the right to access the Todo or not
        if (todo.creator == request.user):
            check = True
        else:
            for i in todo.collaborator.all():
                check = True if i == request.user else check
        # If user is not related to the Todo, forbid the request     
        if check == False:
            return Response(status = status.HTTP_403_FORBIDDEN)

        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            todo = Todo.objects.get(id= id)
        except Todo.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
        # Each Todo is accessible only to its creator and collaborators
        check = False # To check if the user has the right to access the Todo or not
        if (todo.creator == request.user):
            check = True
        else:
            for i in todo.collaborator.all():
                check = True if i == request.user else check
        # If user is not related to the Todo, forbid the request     
        if check == False:
            return Response(status = status.HTTP_403_FORBIDDEN)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        # ONLY CREATOR CAN DO UPDATE ALL FIELDS
        try:
            todo = Todo.objects.get(id= id)
        except Todo.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

        if (todo.creator != request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        # Update title if it is given
        if 'title' in request.data.keys():
            todo.title = request.data['title']
            
        # Update collaborators if asked to
        if 'collaborators' in request.data.keys():
            all = todo.collaborator.all()
            for something in all:
                todo.collaborator.remove(something)
            colab = request.data['collaborators']
            for x in colab.split(','):
                y = User.objects.filter(username = x)
                # If no such user is found, discard it
                # Else append the username to the list and add the collaborator
                if y.count() != 0:
                    todo.collaborator.add(y.first())
        todo.save()

        # Serialize the Todo
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data, status = status.HTTP_200_OK)
        
    def patch(self, request, id):
        try:
            todo = Todo.objects.get(id= id)
        except Todo.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
        # Each Todo is accessible only to its creator and collaborators
        check = False # To check if the user has the right to access the Todo or not
        if (todo.creator == request.user):
            check = True
        else:
            for i in todo.collaborator.all():
                check = True if i == request.user else check
        # If user is not related to the Todo, forbid the request     
        if check == False:
            return Response(status = status.HTTP_403_FORBIDDEN)

        # Update title if it is given
        if 'title' in request.data.keys():
            todo.title = request.data['title']

        # Update the collaborators if it is asked and the user is the creator of the Todo
        if 'collaborators' in request.data.keys() and todo.creator == request.user:
            colab = request.data['collaborators']
            for x in colab.split(','):
                y = User.objects.filter(username = x)
                # If no such user is found, discard it
                # Else append the username to the list and add the collaborator
                if y.count() != 0:
                    todo.collaborator.add(y.first())
        todo.save()

        # Serialize the Todo
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data, status = status.HTTP_200_OK)