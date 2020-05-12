from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username = serializers.CharField(min_length=1)
    password = serializers.CharField(min_length=1)

    def authenticator(self):
        data = self.data
        user = authenticate(username= data['username'], password= data['password'])
        if user is not None:
            return user
        else:
            return False
       


class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality
    first_name = serializers.CharField(max_length = 20, min_length = 1)
    last_name = serializers.CharField(max_length = 20, min_length = 1)
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=255, min_length= 1)
    password = serializers.CharField(max_length=255, min_length= 1)

    class Meta:
        fields = ('first_name', 'last_name' , 'email', 'username','password')
    def do(self):
        username = self.data['username']
        password = self.data['password']
        first_name = self.data['first_name']
        last_name = self.data['last_name']
        user = User.objects.create(username = username, first_name = first_name, last_name = last_name)
        user.set_password(password)
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150, min_length= 1)


    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name' , 'email', 'username')