from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Users


class UsersSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True, validators=[validate_password])
    password = serializers.CharField(write_only=True, max_length=200)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20)
    password_confirm = serializers.CharField(max_length=20)

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'username': {"required": True},
            'email': {"required": True},
        }

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Password Do not Match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = Users(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
