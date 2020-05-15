from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404


"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title',)


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

    class Meta:
        model = Todo
        fields = ('id', 'title',)


class TodoCollaboratorSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=250)

    def add(self, id):
        todo = get_object_or_404(Todo, id=id)
        self.is_valid()
        username = self.validated_data['username']
        user = User.objects.filter(username=username)
        if not user:
            raise serializers.ValidationError("The user doesn't exsist.")
        else:
            todo.collaborator.add(user[0])
            todo.save()

    def remove(self, id):
        todo = get_object_or_404(Todo, id=id)
        self.is_valid()
        username = self.validated_data['username']
        user = User.objects.filter(username=username)
        if not user:
            raise serializers.ValidationError("The user doesn't exsist.")
        else:
            todo.collaborator.remove(user[0])
            todo.save()
