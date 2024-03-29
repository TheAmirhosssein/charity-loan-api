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
    user_full_name = serializers.CharField(source="user")

    class Meta:
        model = models.PaymentRequest
        fields = [
            "paid_price",
            "paid_date_jalali",
            "is_confirmed",
            "payment_request_attachment",
            "user",
            "user_full_name",
        ]
