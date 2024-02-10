from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "personal_code",
            "phone_number",
            "first_name",
            "last_name",
            "gender",
            "avatar",
            "email",
        ]


class UserInfoSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="get_gender_display")

    class Meta:
        model = User
        fields = [
            "id",
            "personal_code",
            "phone_number",
            "first_name",
            "last_name",
            "gender",
            "avatar",
            "email",
            "date_joined",
        ]
