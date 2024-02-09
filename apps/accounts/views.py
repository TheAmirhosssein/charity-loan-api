from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from apps.accounts import serializers

User = get_user_model()


class UserAdminVS(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserInfoSerializer
