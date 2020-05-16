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
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

class TodoView(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=TodoCollaborativeGet
    def get(self,request):
        todo_o=Todo.objects.filter(creator=User.objects.get(username=self.request.user.username))
        todo_c=set()
        for todos in Todo.objects.all():
            if todos.colaborators.filter(username=request.user.username).count()>0:
                todo_c.add(todos)
        serializer_o=TodoSerializer(todo_o,many=True)
        serializer_c=TodoSerializer(todo_c,many=True)
        todolist={
            'collaborations': serializer_c.data,
            'created': serializer_o.data
        }
        serializer=self.get_serializer(data=todolist)
        serializer.is_valid(raise_exception=True) 
        return Response(serializer.data)
class SpecificTodoView(generics.RetrieveAPIView):
    serializer_class=SpecificTodoSerializer
    def get(self,request,id):
        #add try catch
        todo_object = Todo.objects.get(id=id)
        serializer = self.get_serializer(todo_object)
        return Response(serializer.data)
    def put(self,request,id):
        todo_object=Todo.objects.get(id=id)
        todo_object.title=request.data['title']
        todo_object.save(update_fields=['title'])
        serializer = self.get_serializer(todo_object)
        return Response(serializer.data)

    def patch(self,request,id):
        todo_object=Todo.objects.get(id=id)
        todo_object.title=request.data['title']
        todo_object.save(update_fields=['title'])
        serializer = self.get_serializer(todo_object)
        return Response(serializer.data)
    def delete(self,request,id):
        todo_object=Todo.objects.get(id=id)
        todo_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class collaboratorsView(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=ColabSerializer
    def post(self,request,id):
        serializer = self.get_serializer(request.data)
        todo=Todo.objects.get(id=id)
        if todo.creator==request.user:
            todo.colaborators.add(User.objects.get(username=serializer.data['username']))
            return Response({"details":"Coloborator added"})
        else:
            return Response({"Error":"You are not The owner Of This Todo"})
    def patch(self,request,id):
        serializer = self.get_serializer(request.data)
        todo=Todo.objects.get(id=id)
        if todo.creator==request.user:
            todo.colaborators.remove(User.objects.get(username=serializer.data['username']))
            return Response({"details":"Coloborator Removed"})
        else:
            return Response({"Error":"You are not The owner Of This Todo"}) 