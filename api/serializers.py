from rest_framework import serializers
from .models import Todo
from collections import OrderedDict
from django.contrib.auth.models import User

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class TodoGetSerializer(serializers.ModelSerializer):
    # We only need to show usernames of the users
    creator = UsernameSerializer(read_only = True)
    collaborator = UsernameSerializer(read_only=True, many=True)

    class Meta:
        model = Todo
        fields = ('id', 'title', 'creator', 'collaborator')
        ordering = '-id'

class TodoCreateSerializer(serializers.ModelSerializer):
    collaborators = serializers.CharField(required = False, help_text = "Enter usernames separated by comma. Leave empty if no collaborators")

    def save(self):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        todo = Todo.objects.create(creator = user, title = title)
        return todo.id

    def addCollaborators(self, id ,colab):
        data = self.validated_data
        todo = Todo.objects.get(id = id)
        # List for appending the usernames of Collaborators
        data['collaborators'] = []
        # Iterate through all usernames and add the collaborators
        for x in colab.split(','):
            y = User.objects.filter(username = x)
            # If no such user is found, discard it
            # Else append the username to the list and add the collaborator
            if y.count() != 0:
                data['collaborators'].append({'username': x})
                todo.collaborator.add(y.first())
    
    class Meta:
        model = Todo
        fields = ('title','collaborators')

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

class TodoDetailSerializer(serializers.ModelSerializer):
    # We only need to show usernames of the users
    collaborator = UsernameSerializer(read_only=True, many=True)
    creator = UsernameSerializer(read_only=True)
    class Meta:
        model = Todo
        fields = ('id','creator','title','collaborator')

class Todoializer(serializers.Serializer):
    # We only need to show usernames of the users
    title = serializers.CharField(required = False)
    collaborators = serializers.CharField(required = False, help_text= "Enter usernames separated by comma")
    class Meta:
        fields = ('title', 'collaborators')