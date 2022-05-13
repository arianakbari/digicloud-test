from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUserView

urlpatterns = [
    path("register", RegisterUserView.as_view()),
    path("login", TokenObtainPairView.as_view()),
    path("refresh-token", TokenRefreshView.as_view()),
]
