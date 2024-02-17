from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from drf_api_logger.models import APILogsModel
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts import models, serializers
from apps.utils.senders import SendSMS
from apps.api.permissions import IsAdmin

User = get_user_model()


class UserAdminVS(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserInfoSerializer
    permission_classes = [IsAdmin]
    filterset_fields = ["gender"]
    search_fields = [
        "first_name",
        "last_name",
        "phone_number",
        "personal_code",
    ]
    ordering_fields = ["id"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.serializer_class
        else:
            return serializers.CreateUserSerializer


class SendOTP(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = serializers.SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                phone_number=serializer.data["phone_number"],
                personal_code=serializer.data["personal_code"],
            )
            new_otp = models.OTPRequest(user=user)
            new_otp.save()
            SendSMS.send_otp(new_otp.otp, user.phone_number)
            return Response(
                {
                    "response": _("otp code sent"),
                    "key": new_otp.uuid,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyOTP(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = serializers.VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_request = get_object_or_404(
                models.OTPRequest,
                uuid=serializer.data["uuid"],
                otp=serializer.data["otp"],
                verified=False,
            )
            if otp_request.is_expired():
                return Response(
                    {"error": _("code is expired")},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            else:
                otp_request.verify_otp()
                token = RefreshToken.for_user(otp_request.user)
                data = {
                    "refresh": str(token),
                    "access": str(token.access_token),
                    "user": serializers.UserInfoSerializer(
                        otp_request.user,
                    ).data,
                }
                return Response(data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class EditUserInfoAV(RetrieveUpdateAPIView):
    queryset = User
    serializer_class = serializers.ShowUserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return self.serializer_class
        else:
            return serializers.EditUserInfoSerializer

    def get_object(self):
        return self.request.user


class UserLogVS(ReadOnlyModelViewSet):
    serializer_class = serializers.UserLogserializer
    queryset = APILogsModel.objects.all()
    permission_classes = [IsAdmin]
    filter_backends = ["method", "status_code"]


class SMSReportVS(ReadOnlyModelViewSet):
    serializer_class = serializers.SentSMSSerializer
    queryset = models.SentSMS.objects.all()
    permission_classes = [IsAdmin]
    search_fields = ["phone_number"]
    ordering_fields = ["id"]
