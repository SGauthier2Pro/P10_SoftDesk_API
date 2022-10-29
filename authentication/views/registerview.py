from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from authentication.serializers.registerserializer import RegisterSerializer
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer