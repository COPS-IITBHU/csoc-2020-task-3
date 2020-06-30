from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoSerializer,CollaboratorSerializer
from .models import Todo
from rest_framework import mixins
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""
class TodoGetView(generics.GenericAPIView):
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        todo_list = request.user.creator.all()
        serializer = self.get_serializer(todo_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TodoDetailedView(generics.GenericAPIView,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field='id'
    def get(self,request,id):
        user_todo = request.user.creator.all()
        if user_todo.filter(id=id).count() != 0:
            return self.retrieve(request)
        else:
            response = {"Error": "You dont have any todo with the given id"}
            return Response(response,status=status.HTTP_404_NOT_FOUND)


    def put(self,request,id):

        user_todo = request.user.creator.all()
        if user_todo.filter(id=id).count() != 0:
           todo_object = Todo.objects.get(id=id)
           serializer = self.get_serializer(data=request.data)
           if serializer.is_valid(raise_exception=True):
               todo_object.title = serializer.validated_data['title']
               todo_object.save()
               serializer = self.get_serializer(todo_object)
               return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            # return self.update(request,id)
        else:
            response = {"Error": "You dont have any todo with the given id"}
            return Response(response,status=status.HTTP_404_NOT_FOUND) 

    def patch(self,request,id):

        user_todo = request.user.creator.all()
        if user_todo.filter(id=id).count() != 0:
           todo_object = Todo.objects.get(id=id)
           serializer = self.get_serializer(data=request.data)
           if serializer.is_valid(raise_exception=True):
               todo_object.title = serializer.validated_data['title']
               todo_object.save()
               serializer = self.get_serializer(todo_object)
               return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            # return self.update(request,id)
        else:
            response = {"Error": "You dont have any todo with the given id"}
            return Response(response,status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        user_todo = request.user.creator.all()
        if user_todo.filter(id=id).count() != 0:
            self.destroy(request,id)
            response = {"Success":"Successfully deleted the Todo "}
            return Response(response,status=status.HTTP_202_ACCEPTED)
            
        else:
            response = {"Error": "You dont have any todo with the given id"}
            return Response(response,status=status.HTTP_404_NOT_FOUND) 
               



#     def delete(self,request,id):
        
#         return Response(serializer.data,status=status.HTTP_200_OK)
 




class TodoCreateView(generics.GenericAPIView,mixins.CreateModelMixin):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def post(self, request):
        """
        Creates a Todo entry for the logged in user.
        """
        todo_list = request.user.creator.all()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer2 =self.get_serializer(todo_list.last()) 
        return Response(serializer2.data,status=status.HTTP_200_OK)

class TodoCollaboratorsListView(generics.GenericAPIView,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field='id'
    def get(self,request,id):
        user_todo = request.user.creator.all()
        if user_todo.filter(id=id).count() != 0:
            list = []
            for collaborator in user_todo.filter(id=id)[0].collaborators.all():
                list.append(collaborator.username)
            response = {"Collaborators of this to do" : str(list)}
            return Response(response,status=status.HTTP_200_OK)
        else:
            response = {"Error": "You dont have any todo with the given id"}
            return Response(response,status=status.HTTP_404_NOT_FOUND)        
        
class CollabTodo(generics.GenericAPIView,):
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated, )
    def get(self,request):
        todo_collab_list = request.user.collaborators.all()
        if todo_collab_list.count() != 0:  
            serializer = self.get_serializer(todo_collab_list,many=True)    
            return Response(serializer.data,status=status.HTTP_200_OK) 
        response={"Result":"You dont have any collaborations"}
        return Response(response,status=status.HTTP_200_OK) 



class AddCollaborator(generics.GenericAPIView,):
    serializer_class = CollaboratorSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'id'
    def post(self,request,id):
        try:
            todo_object = Todo.objects.get(id=id)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                if todo_object.creator == request.user:
                    data = serializer.validated_data
                    try:
                        user = User.objects.get(username=data['username'])
                        todo_object.collaborators.add(user)
                        print(todo_object.collaborators.all())
                        
                        response = {"Success":"Succesfully added the collaborator"} 
                        return Response(response,status=status.HTTP_200_OK)
                    except ObjectDoesNotExist:
                        response = {"Error":"No user found with that username"} 
                        return Response(response,status=status.HTTP_400_BAD_REQUEST)
                else:
                    response = {"Error":"You are not the creator of this Todo."}
                    return Response(response,status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            response = {"Error":"No todo exists with the id provided"}   
            return Response(response,status=status.HTTP_400_BAD_REQUEST)       

                    
class DeleteCollaborator(generics.GenericAPIView,):
    serializer_class = CollaboratorSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'id'
    def post(self,request,id):
        try:
            todo_object = Todo.objects.get(id=id)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                if todo_object.creator == request.user:
                    data = serializer.validated_data

                    try:
                        user = User.objects.get(username=data['username'])
                        
                        todo_object.collaborators.remove(user)
                        print(user)
                        print(todo_object.collaborators.filter(username=data['username']))
                        
                        response = {"Success":"Succesfully removed the collaborator"} 
                        return Response(response,status=status.HTTP_200_OK)
                    except ObjectDoesNotExist:
                        response = {"Error":"No user found with that username"} 
                        return Response(response,status=status.HTTP_400_BAD_REQUEST)   
                else:
                    response = {"Error":"You are not the creator of this Todo."}
                    return Response(response,status=status.HTTP_400_BAD_REQUEST) 
        except ObjectDoesNotExist:
            response = {"Error":"No todo exists with the id provided"}   
            return Response(response,status=status.HTTP_400_BAD_REQUEST)                                
        

class CollabTodoDetailedView(generics.GenericAPIView,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field='id'
    def get(self,request,id):
        collabs = request.user.collaborators.all()
        if collabs.filter(id=id).count() != 0:
            return self.retrieve(request)
        else:
            response = {"Error": "You are not a collaborator for this todo"}
            return Response(response,status=status.HTTP_404_NOT_FOUND)


    def put(self,request,id):

        collabs = request.user.collaborators.all()
        if collabs.filter(id=id).count() != 0:
           todo_object = Todo.objects.get(id=id)
           serializer = self.get_serializer(data=request.data)
           if serializer.is_valid(raise_exception=True):
               todo_object.title = serializer.validated_data['title']
               todo_object.save()
               serializer = self.get_serializer(todo_object)
               return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            # return self.update(request,id)
        else:
            response = {"Error": "You are not a collaborator for this todo"}
            return Response(response,status=status.HTTP_404_NOT_FOUND) 

    def patch(self,request,id):

        collabs = request.user.collaborators.all()
        if collabs.filter(id=id).count() != 0:
           todo_object = Todo.objects.get(id=id)
           serializer = self.get_serializer(data=request.data)
           if serializer.is_valid(raise_exception=True):
               todo_object.title = serializer.validated_data['title']
               todo_object.save()
               serializer = self.get_serializer(todo_object)
               return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            # return self.update(request,id)
        else:
            response = {"Error": "You are not a collaborator for this todo"}
            return Response(response,status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        collabs = request.user.collaborators.all()
        if collabs.filter(id=id).count() != 0:
            self.destroy(request,id)
            response = {"Success":"Successfully deleted the Todo "}
            return Response(response,status=status.HTTP_202_ACCEPTED)
            
        else:
            response = {"Error": "You are not a collaborator for this todo"}
            return Response(response,status=status.HTTP_404_NOT_FOUND)        
          
                 