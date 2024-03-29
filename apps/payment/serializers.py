from rest_framework import serializers
from apps.payment import models


class PaymentRequestSerializer(serializers.ModelSerializer):
    paid_date_jalali = serializers.DateField(format="YYYY-MM-DD")

    class Meta:
        model = models.PaymentRequest
        fields = ["paid_price", "paid_date_jalali"]


class PaymentRequestInfoSerializer(serializers.ModelSerializer):
    paid_date_jalali = serializers.DateField(format="YYYY-MM-DD")

    class Meta:
        model = models.PaymentRequest
        fields = ["paid_price", "paid_date_jalali", "is_confirmed"]


class PaymentRequestAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentRequestAttachment
        fields = ["payment_request", "attachment"]
        read_only_fields = ["payment_request"]
