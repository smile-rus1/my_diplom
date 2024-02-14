from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views import View

from managers import decorators


class MainPageManagers(View):
    template_name = "managers/index_managers.html"

    @decorators.staff_required
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class MainPageAdmins(View):
    template_name = "managers/index_admins.html"

    @decorators.admin_required
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CreatePageAdmins(View):
    template_name = "managers/create_new_manager.html"

    @decorators.admin_required
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ManagersPageAdmins(View):
    template_name = "managers/administration_of_managers.html"

    @decorators.admin_required
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def logout_manager(request):
    logout(request)
    return redirect("/")
