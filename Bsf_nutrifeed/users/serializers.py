from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,validators =[validate_password])
    password2= serializers.CharField(write_only=True, required=True,label="Confirm Password")

    class Meta:
        model = User
        fields = [
            "id","username","email","first_name","last_name","password","password2","role","phone_number","farm_name","farm_location",
        ]

        extra_kwargs = {"email": {"required": True}}

        def validate(self, attrs):
            if attrs["password"] != ["password2"]:
                raise serializers.ValidationError({"password": "Passwords do not match"})
            return attrs
        
        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id","username","email", "first_name", "last_name","role","phone_number","farm_name", "farm_location","is_verified", "date_joined"
        ]
        read_only_fields = ["id", "username", "is_verified","date_joined"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators =[validate_password])

    def validate_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old Password is incorrect")
        return value
    
    