from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User


"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""
class ColabSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)

class TodoCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        colaborat_users_array=data['colaborators']
        print(colaborat_users_array)
        todo = Todo(creator=user, title=title)
        for cuser in colaborat_users_array:
            todo.colaborators.add(User.objects.get(username=cuser.username))
        todo.save()
        

    colaborators = ColabSerializer(many=True,required=False) 
    class Meta:
        model = Todo
        fields = ('id', 'title','colaborators')
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields = ('id','title')

class SpecificTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields = ('id','title')