from .models import Todo,Collaborate
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CollaborateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User

class AddCollaboration(generics.CreateAPIView):
    
    permission_classes = (IsAuthenticated,)
    
    def post(self,request,id,user,formate=None):
            print(id)
            user = User.objects.get(username=user).pk
            data = {'user' : user , 'title' : id }
            serializer = CollaborateSerializer(data=data)
            creator = Todo.objects.get(pk=id).creator
            if request.user != creator :
               raise PermissionDenied("Access Denied")
            else : 
               if  serializer.is_valid() : 
                 serializer.save()
                 return Response({"collaboration Created ! "},status=status.HTTP_201_CREATED)
               else :
                 return Response(serializer.errors)

class RemoveCollaboration(generics.DestroyAPIView):
            
     permission_classes = (IsAuthenticated,)

     def delete(self,request,id,user,formate=None) :
         user = User.objects.get(username=user).pk
         task = Collaborate.objects.filter(title_id=id,user_id=user) 
         creator = Todo.objects.get(pk=id).creator
         if task.exists() :
            if creator != request.user :
              raise PermissionDenied("Access Denied")
            else :
              task.delete()
              return Response({"Collaboration Removed !"},status= status.HTTP_200_OK)
         else :
            return Response({"detail" : "Not Found !"},status=status.HTTP_400_BAD_REQUEST)


                