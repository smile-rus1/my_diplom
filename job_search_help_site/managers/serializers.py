from rest_framework import serializers

from . import models

from search_site.models import RequestToVerificationUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id", "email")


class ManagerSerializer(UserSerializer):
    last_login = serializers.DateTimeField()

    class Meta:
        model = models.User
        fields = UserSerializer.Meta.fields + ("last_login", )


class RequestVerificationRoleSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RequestToVerificationUser
        fields = "__all__"


class VerificationUserRoleSerializer(serializers.ModelSerializer):
    manager = UserSerializer()
    request_verification = RequestVerificationRoleSerializer()

    phone_number = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    second_name = serializers.CharField(read_only=True)
    date_created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.VerificationUserRole
        fields = "__all__"
