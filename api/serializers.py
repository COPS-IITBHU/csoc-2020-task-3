from rest_framework import serializers
from .models import Todo


"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoListViewSerializer(serializers.ModelSerializer):
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
