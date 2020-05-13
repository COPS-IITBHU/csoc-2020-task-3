from rest_framework import serializers
from .models import Todo
from collections import OrderedDict
from django.contrib.auth.models import User

"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""
class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

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
        data['id']= todo.id
    
    class Meta:
        model = Todo
        fields = ('id', 'title',)


class TodoGetSerializer(serializers.ModelSerializer):
    creator = UsernameSerializer(read_only = True)
    collaborator = UsernameSerializer(read_only=True, many=True)
    class Meta:
        model = Todo
        fields = ('id', 'title', 'creator', 'collaborator')
        ordering = '-id'

class TodoDetailSerializer(serializers.ModelSerializer):
    creator = UsernameSerializer(read_only = True)
    collaborator = UsernameSerializer(read_only=True, many=True)
    class Meta:
        model = Todo
        fields = ('id', 'title', 'creator','collaborator')
    
    def put(self, title):
        data = self.data
        data['title'] = title
        todo = Todo.objects.filter(creator = self.context['request'].user, id= data['id']).first()
        todo.title = title
        todo.save()
        return data

    def patch(self, title):
        data = self.data
        data['title'] = title
        todo = Todo.objects.filter(creator = self.context['request'].user, id= data['id']).first()
        todo.title = title
        todo.save()
        return data

    def delete(self):
        data = self.data
        todo = Todo.objects.filter(creator = self.context['request'].user, id= data['id']).first()
        print("\n\n\n\n", todo.id , todo.title)
        todo.delete()

class CollaboratorSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, min_length= 1)  
    class Meta:
        fields = ('username')

    def do(self, id):
        print('\n\n\n\n----------USERNAME-----------', self.data['username'])
        todo = Todo.objects.filter(id= id).first()
        print("\n\t\t", todo)
        
        todo.collaborator.remove(User.objects.filter(username = self.data['username']).first())
        print('\n\n\nDone\n\n\n')

    def adder(self, id):
        print('\n\n\n\n----------USERNAME-----------', self.data['username'])
        todo = Todo.objects.filter(id= id).first()
        print("\n\t\t", todo, '\t',User.objects.filter(username = self.data['username']).first())
        
        todo.collaborator.add(User.objects.filter(username = self.data['username']).first())
        print('\n\n\nDone\n\n\n')