from django.urls import path
from . import views, api


app_name = 'managers'

urlpatterns = [
    # url-ы
    path("", views.MainPageManagers.as_view(), name="index_managers"),
    path("administrations", views.MainPageAdmins.as_view(), name="index_admins"),
    path("logout_manager/", views.logout_manager, name="logout_manager"),
    path("administrations/create_manager/", views.CreatePageAdmins.as_view(), name="create_manager"),
    path("administration_managers", views.ManagersPageAdmins.as_view(), name="administration_managers"),

    # API
    path("administration/", api.AdminManagersView.as_view(), name="admin_managers"),
    path("administration/<int:manager_id>", api.DetailAdminManagersView.as_view(), name="admin_managers_detail"),
    path("verification-user-role/", api.VerifyUserRoleView.as_view(), name="verification_user_role"),
    path("verification-user-role/<int:verification_user_id>", api.DetailUserRoleView.as_view(), name="verification_user_role_detail"),
    path("verification-user-role/<int:verification_user_id>", api.DetailUserRoleView.as_view(), name="verification_user_role_patch"),

]
