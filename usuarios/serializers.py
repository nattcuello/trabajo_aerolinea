# usuarios/serializers.py
from rest_framework import serializers
from core.serializers_mixins import AuditFieldsSerializer, IntegrityFriendlyMixin
from .models import PerfilUsuario
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class PerfilUsuarioSerializer(IntegrityFriendlyMixin, AuditFieldsSerializer):
    user = UserSerializer(read_only=True)

    class Meta(AuditFieldsSerializer.Meta):
        model = PerfilUsuario
        fields = "__all__"
        read_only_fields = AuditFieldsSerializer.Meta.read_only_fields
