from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User

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
        fields = ('id', 'title',)

class UserObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']

class TodoSerializer(serializers.ModelSerializer):
    collaborators = UserObjectSerializer(many=True, required = False)
    creator = UserObjectSerializer(required = False)
    class Meta:
        model = Todo
        fields = ['id', 'title', 'creator', 'collaborators',]
class TodoUpateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title',)
class CollaboratorSerializer(serializers.ModelSerializer):
    collaborators = UserObjectSerializer(many=True)
    class Meta:
        model = Todo
        fields = ['collaborators']