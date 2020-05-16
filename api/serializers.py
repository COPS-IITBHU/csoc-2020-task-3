from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User


class TodoViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title')


class TodoCreateSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        todo = Todo.objects.create(creator=user, title=title)

    class Meta:
        model = Todo
        fields = ('id', 'title',)


class CollaboratorSerializer(serializers.ModelSerializer):
    collaboratorUsername = serializers.CharField(required=True, max_length=255)

    def add(self, pk):
        todo = Todo.objects.get(pk=pk)
        self.is_valid()
        print(self.validated_data)
        username = self.validated_data['collaboratorUsername']
        user = User.objects.filter(username=username)
        print(user)
        todo.collaborator.add(user[0])
        todo.save()

    def remove(self, pk):
        todo = Todo.objects.get(pk=pk)
        self.is_valid()
        username = self.validated_data['collaboratorUsername']
        user = User.objects.filter(username=username)
        todo.collaborator.remove(user[0])
        todo.save()

    class Meta:
        model = Todo
        fields = ('collaboratorUsername', 'id')
