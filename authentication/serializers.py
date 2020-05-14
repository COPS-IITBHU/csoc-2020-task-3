from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality

    username = serializers.CharField(min_length=1)
    password = serializers.CharField(min_length=1)

    class Meta :
        model = User
        fields = ('username','password')



class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality
    
      name = serializers.CharField(min_length = 1)
      username = serializers.CharField(min_length=1)
      email = serializers.EmailField(max_length = 200)
      password = serializers.CharField(min_length= 1)
      
      class Meta :

        model = User
        fields = ('name','username','email','password')
        extra_kwargs = {'password':{'write_only' : True},} 
      
      def create(self):
            user = User.objects.create(email = self.data['email'],
                    username=self.data['username'],first_name=self.data['name'])
            user.set_password(self.data['password'])   
            user.save()
            return user


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
      
    

    class Meta :
           model = User
           fields = ('id','first_name','email','username')
        