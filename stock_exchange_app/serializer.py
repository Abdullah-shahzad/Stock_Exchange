from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from stock_exchange_app.models import Users, Stocks, Transaction
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password1']

    def validate(self, data):
        """
        Ensure that both password fields match.
        """
        if data['password'] != data['password1']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        """
        Create a new user instance with hashed password.
        """
        password = validated_data.pop('password')
        validated_data.pop('password1')

        # Hash the password before saving the user
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate username and password.
        """
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is inactive")
            else:
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        data["user"] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom Users model to return basic information like balance.
    """
    class Meta:
        model = Users
        fields = ['username', 'balance']


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for Stocks model.
    """
    class Meta:
        model = Stocks
        fields = ['ticker', 'stock_price', 'stock_name']


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction model with read-only 'created_time' field.
    """
    class Meta:
        model = Transaction
        fields = ['user', 'ticker', 'transaction_price', 'transaction_type', 'transaction_volume', 'created_time']
        read_only_fields = ['created_time']
