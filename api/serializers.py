from rest_framework import serializers, exceptions
from .models import Todo, User


"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title','iscreator', 'iscollaborator')
        extra_kwargs = {
            'iscreator': {'read_only': True},
            'iscollaborator': {'read_only': True}
        }


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
        todo = Todo.objects.create(creator=user, title=title, iscreator=True, iscollaborator=False)
        return todo
    
    class Meta:
        model = Todo
        fields = ('id', 'title',)


class AddCollaboratorSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, help_text='Please Enter Email of Collaborator')

    def add_collaborators(self, id, loggedinuser):
        email = self.validated_data['email']
        user = User.objects.filter(email = email)
        
        if user and (str(loggedinuser) != user[0].username):
            todo = Todo.objects.filter(id = id)
            if todo:
                todo[0].Collaborators.add(user[0])
                todo[0].save()
            else:
                raise exceptions.ValidationError("Todo Not Found")
        elif user and (str(loggedinuser) == user[0].username):
            raise exceptions.ValidationError("Sorry, It is creator of Todo")
        else:
            raise exceptions.ValidationError("No user exist")


class RemoveCollaboratorSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True, help_text='Please Enter Email of Collaborator')

    def remove_collaborators(self, id):
        email = self.validated_data['email']
        user = User.objects.filter(email = email)

        if user:
            todo = Todo.objects.filter(id = id)

            if todo and todo[0].Collaborators.filter(username = user[0].username):
                todo[0].Collaborators.remove(user[0])
                todo[0].save()
            elif todo and not todo[0].Collaborators.filter(username = user[0].username):
                raise exceptions.ValidationError("It is not the Collaborator")
            else:
                raise exceptions.ValidationError("Todo Not Found")
        else:
            raise exceptions.ValidationError("No user exist")