from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from .serializers import CreateUserSerializer
# Create your views here.

class RegisterUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer