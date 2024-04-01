from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import get_object_or_404
from apps.api.permissions import IsAdminOrAuthorNested, IsAdminOrReadOnly
from apps.payment import models, serializers


class PaymentRequestUserVS(ModelViewSet):
    serializer_class = serializers.PaymentRequestSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["user", "is_confirmed"]
    ordering_fields = ["id", "paid_price", "paid_date"]
    search_fields = ["paid_price", "paid_date"]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.PaymentRequestInfoSerializer
        elif self.request.user.is_admin_user:
            return serializers.PaymentRequestAdminSerializer
        return self.serializer_class

    def get_queryset(self):
        return models.PaymentRequest.objects.all_admin_filtered_users(
            user=self.request.user, user__pk=self.request.user.pk
        ).prefetch_related("payment_request_attachment")

    def destroy(self, request, *args, **kwargs):
        if self.get_object().is_confirmed:
            return Response(
                {"detail": _("you are not allowed to do this action")},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        update_response = super().update(request, *args, **kwargs)
        payment_request: models.PaymentRequest = self.get_object()
        if self.request.user.is_admin_user:
            if payment_request.is_confirmed:
                payment_request.confirm()
            else:
                payment_request.undo_confirm()
        return update_response


class PaymentRequestAttachmentVS(ModelViewSet):
    serializer_class = serializers.PaymentRequestAttachmentSerializer
    queryset = models.PaymentRequestAttachment.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrAuthorNested]
    user_field = "user"

    def perform_create(self, serializer):
        return serializer.save(payment_request=self.get_parent_object)

    def get_parent_object(self) -> models.PaymentRequest:
        payment_request = get_object_or_404(
            models.PaymentRequest, pk=self.kwargs["payment_request_pk"]
        )
        return payment_request


class PaymentAdminVS(ModelViewSet):
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["user"]
    ordering_fields = ["id", "payment_price", "payment_date"]
    search_fields = ["payment_price", "payment_date"]

    def perform_create(self, serializer):
        return serializer.save(payment_type="MA")

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.PaymentSerializerInfo
        return self.serializer_class

    def get_queryset(self):
        return models.Payment.objects.all_admin_filtered_users(
            user=self.request.user, user_id=self.request.user.pk
        )
