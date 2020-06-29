from rest_framework import serializers
from .models import Todo
from rest_framework.exceptions import ValidationError
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
    
    class Meta:
        model = Todo
        fields = ('id', 'title',)

class TodoSerializer(serializers.ModelSerializer):
    collaborators = serializers.StringRelatedField(many=True, read_only=True)
    creator = serializers.StringRelatedField()
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['id','creator']

class TodoCollaboratorSerializer(serializers.ModelSerializer):
    collaborators = serializers.StringRelatedField(many=True)
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'title', ]
    
    def is_valid(self, raise_exception=True):
        try:
            usernames = self.initial_data['usernames']
        except:
            raise ValidationError({"usernames": "field required"})
        if not isinstance(usernames, list):
            raise ValidationError({"usernames": "array required"})
        if not hasattr(self,'_validated_data'):
            self._validated_data = {}
        
        self.store_users(usernames)

        self._errors = {}
        return True

    def store_users(self, usernames):
        self._validated_data['collaborators'] = []
        for name in usernames:
            try:
                user = User.objects.get(username = name)
            except :
                raise ValidationError({'details':"user does not exist"})
            if self.context['request'].user != user:
                self._validated_data['collaborators'].append(user)

    def update(self, instance, validated_data):
        for user in validated_data['collaborators']:
            if self.context['add']:
                instance.collaborators.add(user)
            else:
                try:
                    instance.collaborators.remove(user)
                except:
                    pass
        instance.save()
        return instance

