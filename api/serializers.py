from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

UserModel = get_user_model()

"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoCreateSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        todo = Todo.objects.create(creator=user, title=title)
        todo.save()

        data = {'id': todo.id, 'title': data['title']}
        return data

    class Meta:
        model = Todo
        fields = ('id', 'title',)


class TodoSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(
        source='creator.username', required=False, read_only=True)

    class Meta:
        model = Todo
        fields = ('id', 'title', 'creator')


class TodoContri(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = contributor
        fields = ('username', 'todo')
        extra_kwargs = {
            'todo': {'required': False, 'read_only': True},
            'username': {'required': True}
        }
