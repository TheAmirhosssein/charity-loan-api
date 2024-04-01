from django.utils.translation import gettext as _
from rest_framework import serializers
from drf_api_logger.models import APILogsModel
from apps.utils.validators import PhoneNumberValidator

from apps.accounts.models import User, SentSMS, Winners


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
            "monthly_payment",
        ]


class UserInfoSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="get_gender_display")
    date_joined = serializers.CharField(source="date_joined_jalali")

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
            "monthly_payment",
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
                _("no user `exists` with entered information")
            )
        elif not user.can_create_otp():
            raise serializers.ValidationError(
                _("pleas wait for a new otp message"),
            )
        else:
            return super().validate(attrs)


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    uuid = serializers.UUIDField()


class EditUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender", "avatar"]
        read_only_fields = ["monthly_payment"]


class ShowUserInfoSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="get_gender_display")
    is_admin_user = serializers.BooleanField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "gender",
            "avatar",
            "personal_code",
            "phone_number",
            "is_admin_user",
        ]


class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APILogsModel
        fields = ["body", "api", "method", "status_code"]


class SentSMSSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="get_user")
    reason = serializers.CharField(source="get_reason_display")
    created_at = serializers.CharField(source="created_at_jalali")
    updated_at = serializers.CharField(source="updated_at_jalali")

    class Meta:
        model = SentSMS
        exclude = ["deleted", "deleted_at"]


class SendSMSSerializer(serializers.Serializer):
    phone_numbers = serializers.ListField(child=serializers.CharField())
    text = serializers.CharField()

    def validate_phone_numbers(self, phone_numbers):
        validator = PhoneNumberValidator()
        for phone_number in phone_numbers:
            validator(phone_number)
        return phone_numbers


class WinnersInfo(serializers.ModelSerializer):
    created_at = serializers.CharField(source="created_at_jalali")
    updated_at = serializers.CharField(source="updated_at_jalali")
    user_full_name = serializers.StringRelatedField(source="user")

    class Meta:
        model = Winners
        fields = ["id", "user", "created_at", "updated_at", "user_full_name"]


class LotterySerializer(serializers.Serializer):
    count = serializers.IntegerField()
    duplicate_user = serializers.BooleanField()
