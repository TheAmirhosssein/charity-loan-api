from rest_framework import serializers
from apps.payment import models


class PaymentRequest(serializers.ModelSerializer):
    paid_date_jalali = serializers.DateField(format="YYYY-MM-DD")

    class Meta:
        model = models.PaymentRequest
        fields = ["paid_price", "paid_date_jalali"]


class PaymentRequestInfo(serializers.ModelSerializer):
    paid_date_jalali = serializers.DateField(format="YYYY-MM-DD")

    class Meta:
        model = models.PaymentRequest
        fields = ["paid_price", "paid_date_jalali", "is_confirmed"]
