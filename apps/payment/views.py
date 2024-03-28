from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.payment import models, serializers


class PaymentRequestUser(ModelViewSet):
    serializer_class = serializers.PaymentRequest
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return models.PaymentRequest.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().is_confirmed:
            return Response(
                {"response": _("you are not allowed to do this action")},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)
