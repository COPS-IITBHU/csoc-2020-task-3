from rest_framework import serializers
from .models import Todo,Collaborator
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldError

"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoCreateSerializer(serializers.ModelSerializer):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """

    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        todo = Todo.objects.create(creator=user, title=title)
        return todo

    class Meta:
        model = Todo
        fields = ('id','title')


class TodoListSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(max_length=100)
    class Meta:
        model = Todo
        fields = ('id', 'user_type' , 'title')



class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id','title')


    def update(self,id):
        print(self.validated_data.get('title'))
        instance= Todo.objects.get(id=id)
        instance.title = self.validated_data['title']
        instance.save()
        return instance

class AddCollaboraorSerializer(serializers.Serializer):
    collaborator_username = serializers.CharField(max_length=255,min_length=1)





class DeleteCollaboraorSerializer(serializers.Serializer):
    collaborator_username = serializers.CharField(max_length=255,min_length=1)
    def delete(self,id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            error = {'message': "Todo doesn't exists!"}
            raise serializers.ValidationError(error)
        try:
            user = User.objects.get(username=self.validated_data['collaborator_username'])
        except:
            error = {'message': "Collaboration User doesn't exists!"}
            raise serializers.ValidationError(error)
        try :
            instance = Collaborator.objects.get(collaborator=user,todo=todo)
            instance.delete()
        except:
            error = {'message': "User not Collaborated"}
            raise serializers.ValidationError(error)