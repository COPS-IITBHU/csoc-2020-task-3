from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User



"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""
class CollaboratorSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    


class TodoSerializer(serializers.ModelSerializer):
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

    def create(self,validated_data):
        return Todo.objects.create(validated_data)    
    
    class Meta:
        model = Todo
        fields = ('id', 'title',)
