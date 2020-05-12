from rest_framework import serializers
from .models import Todo, contributor


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
    class Meta:
        model = Todo
        fields = ('id', 'title',)


class TodoContri(serializers.ModelSerializer):
    class Meta:
        model = contributor
