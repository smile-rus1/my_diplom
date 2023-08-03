from django.contrib import admin

from search_site.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", )


admin.register(CustomUser, CustomUserAdmin)
