from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.accounts.models import User


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


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    personal_code = serializers.CharField()

    def validate(self, attrs: dict) -> None:
        user = User.objects.filter(
            personal_code=attrs["personal_code"],
            phone_number=attrs["phone_number"],
        ).first()
        if user is None:
            raise serializers.ValidationError(
                _("no user exists with entered information")
            )
        elif not user.can_create_otp():
            raise serializers.ValidationError(
                _("pleas wait for a new otp message"),
            )
        else:
            return super().validate(attrs)
