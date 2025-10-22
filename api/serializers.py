from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        )
    
    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'password', 
                  'first_name', 'last_name','is_staff', 'is_active']
        read_only_fields = ['pk']