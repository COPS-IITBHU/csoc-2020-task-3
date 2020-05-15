from rest_framework import serializers
from .models import Todo


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
