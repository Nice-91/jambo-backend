from rest_framework import serializers
from .models import User, Device


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_verified']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_id', 'is_verified', 'created_at']
        read_only_fields = ['is_verified', 'created_at']
