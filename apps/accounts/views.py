from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from apps.accounts import serializers

User = get_user_model()


class CreateUserAV(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.CreateUser
