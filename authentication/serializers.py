from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # Fields for serializer
    username = serializers.CharField(min_length = 1)
    password = serializers.CharField(min_length = 1)
    class Meta:
        fields = ('username','password')

    # Function to check authentication for credentials
    def authenticator(self):
        user = authenticate(username = self.data['username'], password = self.data['password'])
        if user is not None:
            return user
        else:
            return None

class RegisterSerializer(serializers.Serializer):
    # Fields for Serializer
    first_name = serializers.CharField(max_length = 20, min_length = 1)
    last_name = serializers.CharField(max_length = 20, min_length = 1)
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=255, min_length= 1)
    password = serializers.CharField(max_length=255, min_length= 1)

    class Meta:
        fields = ('first_name', 'last_name' , 'email', 'username','password')

    def register(self):
        username = self.data['username']
        first_name = self.data['first_name']
        last_name = self.data['last_name']
        # Create user
        user = User.objects.create(username = username, first_name = first_name, last_name = last_name)
        user.email = self.data['email']
        user.set_password(self.data['password'])
        user.save()
        # Return the user for token generation
        return user



class UserSerializer(serializers.ModelSerializer):
    # Fields for serializer
    id = serializers.IntegerField()
    name = serializers.CharField(source = 'get_full_name')
    email = serializers.EmailField(max_length = 254)
    username = serializers.CharField(max_length = 150, min_length = 1)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username')