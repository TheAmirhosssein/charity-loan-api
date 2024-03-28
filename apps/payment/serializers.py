from rest_framework import serializers
from apps.payment import models


class PaymentRequest(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentRequest
        fields = ["paid_price", "paid_date"]
