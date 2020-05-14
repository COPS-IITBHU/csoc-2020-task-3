from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TodoCreateSerializer,TaskSerializer,TaskListSerializer
from django.http import Http404
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
        if serializer.is_valid() : 
          task =   serializer.save()
          return Response({"id" : task.id,"title" : task.title},status=status.HTTP_200_OK)
        else : 
          return Response(status=status.HTTP_400_BAD_REQUEST)  

class TodoListView(APIView):

      permission_classes = (permissions.IsAuthenticated,)
      
      def get(self,request):
          todos = Todo.objects.filter(creator = request.user.id)
          serializer =TaskListSerializer(todos,many=True)
          return Response(serializer.data,status=status.HTTP_200_OK)    


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TaskSerializer 
    
    def get_object(self,id):
        try :
            return Todo.objects.get(pk=id)
        except :
            raise Http404

    def get(self,request,id,formate=None):
        task = self.get_object(id)
        if task.creator != request.user :
          return Response({"detail" : "Not Found ! "})
        else :    
          serializer =  TaskSerializer(task)
          return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,id,formate=None):
        task = self.get_object(id)
        if task.creator != request.user :
          return Response({"detail" : "Not Found ! "})
        else :    
          serializer =  TaskSerializer(task,data=request.data)           
          if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data) 
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,formate=None) :
        task = self.get_object(id)
        if task.creator != request.user :
          return Response({"detail" : "Not Found ! "})
        else :    
          task.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)    
     
    def patch(self,request,id,formate=None):
        task = self.get_object(id)
        if task.creator != request.user :
          return Response({"detail" : "Not Found ! "})
        else :    
          serializer =  TaskSerializer(task,data=request.data)           
          if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data) 
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
