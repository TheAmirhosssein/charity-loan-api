from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.accounts import serializers, models
from django.utils.translation import gettext as _


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
            return Response(
                {"response": _("otp code sent")},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
