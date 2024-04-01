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
from apps.api.permissions import IsAdmin, IsAdminOrReadOnly
from apps.utils.date import range_to_end_month
from apps.utils.senders import SendSMS

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
                    "detail": _("otp code sent"),
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
    serializer_class = serializers.UserLogSerializer
    queryset = APILogsModel.objects.all()
    permission_classes = [IsAdmin]
    filterset_fields = ["method", "status_code"]


class SMSReportVS(ReadOnlyModelViewSet):
    serializer_class = serializers.SentSMSSerializer
    queryset = models.SentSMS.objects.all()
    permission_classes = [IsAdmin]
    search_fields = ["phone_number"]
    filterset_fields = ["reason"]
    ordering_fields = ["id"]


class SendSMSAV(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = serializers.SendSMSSerializer(data=request.data)
        if serializer.is_valid():
            SendSMS.multiple_send(
                serializer.validated_data["phone_numbers"],
                serializer.validated_data["text"],
            )
            return Response({"detail": _("SMS sent")}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class WinnersVS(ModelViewSet):
    queryset = models.Winners.objects.all()
    serializer_class = serializers.WinnersInfo
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["date"]
    filterset_fields = ["user"]
    ordering_fields = ["id"]

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.GET.get("date")
        if date in ["", None]:
            return queryset
        try:
            gregorian_date = range_to_end_month(date)
            return queryset.filter(
                created_at__range=[gregorian_date[0], gregorian_date[1]]
            )
        except Exception:
            return queryset.none()


class Lottery(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = serializers.LotterySerializer(data=request.data)
        if serializer.is_valid():
            try:
                winners = User.objects.lottery(
                    is_admin=False, count=serializer.validated_data["count"]
                )
            except ValueError as e:
                return Response({"detail": str(e)}, status.HTTP_400_BAD_REQUEST)
            serialized_winners = serializers.UserInfoSerializer(winners, many=True).data
            return Response(serialized_winners, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
