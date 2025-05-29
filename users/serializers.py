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
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ('id', 'username', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm') 
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        return user
