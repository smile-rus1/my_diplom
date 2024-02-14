from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import decorators, models, serializers

from .repository import *
from .services import *


class BaseView(APIView):
    """
    Base view, which realization DI(or IoC).
    """
    def __init__(self, repository: base_repository.BaseRepository):
        self.repository = repository


class AdminManagersView(BaseView):
    """
    API endpoint which create a manager.
    """
    def __init__(self, repository=admin_manager_repository.RepositoryAdminManager(models.User)):
        super().__init__(repository)

    @decorators.admin_required
    def get(self, request, *args, **kwargs):
        queryset = self.repository.get_all_managers()
        serializer = serializers.ManagerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.admin_required
    def post(self, request):
        manager = self.repository.create_model(**request.data)

        if manager is None:
            return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Создано"}, status=status.HTTP_201_CREATED)


class DetailAdminManagersView(BaseView):
    """
    API endpoint that show manager info.
    """

    def __init__(self, repository=admin_manager_repository.RepositoryAdminManager(models.User)):
        super().__init__(repository)

    @decorators.admin_required
    def get(self, request, manager_id: int, *args, **kwargs):
        return

    @decorators.admin_required
    def patch(self, request, manager_id: int, *args, **kwargs):
        return

    def delete(self, request, manager_id: int, *args, **kwargs):
        self.repository.delete_model_instance(id=int(manager_id))
        return Response({"message": "Instance delete"}, status=status.HTTP_204_NO_CONTENT)


class VerifyUserRoleView(BaseView):
    """
    API endpoint that shows request to verification role of user.
    """
    def __init__(
            self,
            repository=repository_verification_user.RepositoryVerificationUserRole(models.VerificationUserRole)
    ):
        super().__init__(repository)

    @decorators.staff_required
    def get(self, request, *args, **kwargs):
        filters = request.GET.dict()
        queryset = self.repository.get_verification_user_roles_for_manager(
            manager=request.user,
            filters=filters
        )
        serializer = serializers.VerificationUserRoleSerializer(queryset, many=True)

        if serializer is None:
            return Response({"message": "Не удалось найти!"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailUserRoleView(BaseView):
    def __init__(
            self,
            repository=repository_verification_user.RepositoryVerificationUserRole(models.VerificationUserRole)
    ):
        super().__init__(repository)

    @decorators.staff_required
    def get(self, request, verification_user_id: int, *args, **kwargs):
        queryset = self.repository.get_verification_user_role_by_id(verification_user_id, request.user)
        if not queryset:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.VerificationUserRoleSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.staff_required
    def patch(self, request, verification_user_id: int):
        instance = self.repository.get_verification_user_role_by_id(verification_user_id, request.user)
        if instance is None:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        verify = verification_user_service.VerificationUserService.confirm_user_role(instance, request.data)
        if verify is None:
            return Response({"message": "Failed to verify role, please try again"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.VerificationUserRoleSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
