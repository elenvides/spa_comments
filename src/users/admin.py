from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["password", "groups", "user_permissions"]
    readonly_fields = [
        "id",
        "is_superuser",
        "is_staff",
        "email"
    ]
    list_filter = ["role"]
    list_display = ["email", "username", "role"]
    search_fields = ["email", "username"]
