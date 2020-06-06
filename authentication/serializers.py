from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)



class RegisterSerializer(serializers.ModelSerializer):
    # TODO: Implement register functionality
    name = serializers.CharField(source='first_name', max_length=150)
    email = serializers.EmailField(max_length=255, required = True, allow_blank=False)
    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password']
        extra_kwargs = {'password':{'write_only':True}}
    def create(self, validated_data):
        user = User(
            first_name = validated_data['first_name'],
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
        )
        user.set_password((validated_data['password']))
        user.save()
        return user
        
class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    name = serializers.CharField(source='first_name', max_length=150, required=False)
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username']