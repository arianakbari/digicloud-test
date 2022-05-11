from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = ["id", "username", "password"]