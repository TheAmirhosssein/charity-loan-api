from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from apps.accounts import serializers

User = get_user_model()


class UserAdminVS(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserInfoSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.serializer_class
        else:
            return serializers.CreateUserSerializer
