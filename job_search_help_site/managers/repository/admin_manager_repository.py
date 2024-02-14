from django.db import transaction, IntegrityError

from .base_repository import BaseRepository


class RepositoryAdminManager(BaseRepository):
    """
    Repository of model CustomUser which create a 'manager'(user which have permissions is_staff).
    """
    def get_all_managers(self) -> list:
        return self.get_all().filter(is_staff=True, is_superuser=False)

    def create_model(self, **models_data):
        """
        Create a manager in model CustomUser.
        """
        with transaction.atomic():
            try:
                manager, created = self.model.objects.get_or_create(email=models_data.get("email"))

                if not created:
                    raise IntegrityError("User with this email exists")

                manager.set_password(models_data.get("password"))
                manager.is_active = True
                manager.is_staff = True
                manager.save()

                return manager

            except IntegrityError as IE:
                print(f"Exception {IE}")

            except Exception as e:
                print(f"Exception in create model {e}")

        return None

    def delete_model_instance(self, **criteria):
        """
        Delete managers by received param.
        """
        super().delete_model_instance(**criteria)

