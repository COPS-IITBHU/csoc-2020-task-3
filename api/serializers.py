from rest_framework import serializers
from . models import Todo

class TodoCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        todo = Todo.objects.create(creator=user, title=title)
        return {
            'id':todo.id,
            'title':todo.title
        }

    class Meta:
        model = Todo
        fields = ('id', 'title',)

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields=('id','title')

class CollaboratorSerializer(serializers.Serializer):
    username=serializers.CharField()

    def add(self, id):
        todo=Todo.objects.get(id=id)
        username=self.validated_data['username']
        user=User.objects.filter(username=username)
        todo.collaborator.add(user[0])
        todo.save()

    def remove(self, id):
        todo=Todo.objects.get(id=id)
        username=self.validated_data['username']
        user=User.objects.filter(username=username)
        todo.collaborater.remove(user[0])
        todo.save()

    class Meta:
        model=Todo
        fields=('id', 'username')        