from rest_framework import serializers
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    # TODO: Implement register functionality
    email = serializers.EmailField()
    name = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = ('id','name', 'email', 'username', 'password')

    def create(self, validated_data, *args, **kwargs):
        print(validated_data)
        user = User.objects.create(
            email = validated_data['email'],
            username = validated_data['username'],
            first_name = validated_data['first_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    # class Meta:
    #     model = User
    #     fields = ('id', 'first_name', 'email', 'username')
    pass
    