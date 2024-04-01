from rest_framework import serializers
from apps.payment import models


class PaymentRequestSerializer(serializers.ModelSerializer):
    paid_date_jalali = serializers.DateField(format="YYYY-MM-DD")

    class Meta:
        model = models.PaymentRequest
        fields = ["paid_price", "paid_date_jalali"]


class PaymentRequestAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentRequestAttachment
        fields = ["id", "payment_request", "attachment"]
        read_only_fields = ["payment_request", "id"]


class PaymentRequestInfoSerializer(serializers.ModelSerializer):
    paid_date_jalali = serializers.DateField(format="YYYY-MM-DD")
    payment_request_attachment = PaymentRequestAttachmentSerializer(
        many=True, read_only=True
    )
    user_full_name = serializers.StringRelatedField(source="user")

    class Meta:
        model = models.PaymentRequest
        fields = [
            "id",
            "paid_price",
            "paid_date_jalali",
            "is_confirmed",
            "payment_request_attachment",
            "user",
            "user_full_name",
        ]


class PaymentRequestAdminSerializer(serializers.ModelSerializer):
    paid_date_jalali = serializers.DateField(format="YYYY-MM-DD")

    class Meta:
        model = models.PaymentRequest
        fields = ["paid_price", "paid_date_jalali", "is_confirmed"]


class PaymentSerializerInfo(serializers.ModelSerializer):
    payment_date_jalali = serializers.DateField(format="YYYY-MM-DD")
    user_full_name = serializers.StringRelatedField(source="user")
    payment_type = serializers.CharField(source="get_payment_type_display")

    class Meta:
        model = models.Payment
        fields = [
            "id",
            "payment_price",
            "payment_date_jalali",
            "user",
            "user_full_name",
            "payment_type",
            "other_info",
            "created_at_jalali",
            "updated_at_jalali",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    payment_date_jalali = serializers.DateField(format="YYYY-MM-DD")

    class Meta:
        model = models.Payment
        fields = [
            "payment_price",
            "payment_date_jalali",
            "user",
        ]
