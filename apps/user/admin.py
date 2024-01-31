from django.contrib import admin
from apps.user.models import User

# Register your models here.

@admin.register(User)
# admin.site.register(User)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "username",
                    "first_name", "last_name", "phone",
                    "is_staff", "is_superuser",
                    "is_verified", "is_active",
                    "date_joined", "last_login", ]

    list_filter = ["phone",
                   "is_staff", "is_superuser",
                   "is_verified", "is_active",
                   "date_joined", "last_login", ]

    search_fields = ["email", "username",
                   "first_name", "last_name", "phone",
                   "is_staff", "is_superuser",
                   "is_verified", "is_active",
                   "date_joined", "last_login", ]
