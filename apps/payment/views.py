from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404, get_list_or_404

from apps.payment import models, serializers


class PaymentRequestUserVS(ModelViewSet):
    serializer_class = serializers.PaymentRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.PaymentRequestInfoSerializer
        return self.serializer_class

    def get_queryset(self):
        return models.PaymentRequest.objects.filter(
            user=self.request.user
        ).prefetch_related("payment_request_attachment")

    def destroy(self, request, *args, **kwargs):
        if self.get_object().is_confirmed:
            return Response(
                {"response": _("you are not allowed to do this action")},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class PaymentRequestAttachmentVS(ModelViewSet):
    serializer_class = serializers.PaymentRequestAttachmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request = get_object_or_404(
            models.PaymentRequest,
            user=self.request.user,
            pk=self.kwargs["payment_request_pk"],
        )
        return serializer.save(payment_request=request)

    def get_queryset(self):
        return get_list_or_404(
            models.PaymentRequestAttachment.objects,
            payment_request__user=self.request.user,
            payment_request__pk=self.kwargs["payment_request_pk"],
        )
