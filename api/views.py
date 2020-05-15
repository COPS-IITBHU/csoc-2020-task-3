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
        data=serializer.validated_data
        user = serializer.context['request'].user
        title = data['title']
        colaborat_users_array=data['colaborators']
        todo = Todo(creator=user, title=title)
        todo.save()
        for cuser in colaborat_users_array:
            todo.colaborators.add("da")
        todo.save()
        response_data={"id":Todo.objects.get(title=serializer.data['title']).id,"title":Todo.objects.get(title=serializer.data['title']).title}
        return Response(response_data,status=status.HTTP_200_OK)

class TodoView(generics.ListAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=TodoSerializer
    def get_queryset(self):
        todolist=Todo.objects.filter(creator=self.request.user)
        return todolist
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