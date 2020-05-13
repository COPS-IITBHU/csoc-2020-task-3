from rest_framework import serializers
from .models import Todo
from collections import OrderedDict
from django.contrib.auth.models import User

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class TodoCreateSerializer(serializers.ModelSerializer):
    collaborators = serializers.CharField(required = False, help_text = "Enter usernames separated by comma. Leave empty if no collaborators")

    def save(self, colab):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        # Create the todo
        todo = Todo.objects.create(creator = user, title = title)
        data['id']= todo.id
        # List for appending the usernames of Collaborators
        data['collaborators'] = []
        # Iterate through all usernames and add the collaborators
        for x in colab['username'].split(','):
            y = User.objects.filter(username = x)
            # If no such user is found, discard it
            # Else append the username to the list and add the collaborator
            if y.count() != 0:
                data['collaborators'].append({'username': x})
                todo.collaborator.add(y.first())
    

    class Meta:
        model = Todo
        fields = ('id', 'title','collaborators')


class TodoGetSerializer(serializers.ModelSerializer):
    # We only need to show usernames of the users
    creator = UsernameSerializer(read_only = True)
    collaborator = UsernameSerializer(read_only=True, many=True)

    class Meta:
        model = Todo
        fields = ('id', 'title', 'creator', 'collaborator')
        ordering = '-id'

class TodoDetailSerializer(serializers.ModelSerializer):
    # We only need to show usernames of the users
    creator = UsernameSerializer(read_only = True)
    collaborator = UsernameSerializer(read_only=True, many=True)

    class Meta:
        model = Todo
        fields = ('id', 'title', 'creator','collaborator')
    
    def put(self, title):
        data = self.data
        data['title'] = title
        # Get the todo 
        todo = Todo.objects.get(id= data['id'])
        todo.title = title
        todo.save()
        return data

    def patch(self, title):
        data = self.data
        # Update the title in serializer data
        data['title'] = title
        # Update the title in the model object
        todo = Todo.objects.get(id= data['id'])
        todo.title = title
        todo.save()
        # Return the data
        return data

    def delete(self):
        data = self.data
        todo = Todo.objects.get(id= data['id'])
        todo.delete()

class CollaboratorSerializer(serializers.Serializer):
    usernames = serializers.CharField(max_length=255, min_length= 1, help_text = "Enter usernames separated by comma")  
    class Meta:
        fields = ('usernames')

    def remover(self, id):
        colab = self.data['usernames'].split(',')
        todo = Todo.objects.get(id= id)
        # List for adding the collaborators
        for x in colab:
            y = User.objects.filter(username = x)
            # If no such user is found, discard it
            if y.count() != 0:
                todo.collaborator.remove(y.first())

    def adder(self, id):
        todo = Todo.objects.get(id= id)
        colab = self.data['usernames'].split(',')
        # List for adding the collaborators
        for x in colab:
            y = User.objects.filter(username = x)
            # If no such user is found, discard it
            if y.count() != 0:
                todo.collaborator.add(y.first())