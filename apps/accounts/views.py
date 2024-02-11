from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.accounts import models, serializers
from apps.utils.senders import SendSMS

User = get_user_model()


class UserAdminVS(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserInfoSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.serializer_class
        else:
            return serializers.CreateUserSerializer


class SendOTP(APIView):
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
                # todo : return jwt codes
                return Response("Login Succeed")
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
