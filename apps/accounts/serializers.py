from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "personal_code",
            "phone_number",
            "first_name",
            "last_name",
            "gender",
        ]
