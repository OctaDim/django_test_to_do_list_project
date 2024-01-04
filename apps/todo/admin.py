from django.contrib import admin

from apps.todo.models import (Task, Category, Status, SubTask, User)


# Register your models here.

# admin.site.register(Task)
# admin.site.register(Category)
# admin.site.register(Status)
# admin.site.register(SubTask)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title",
                    "category",
                    "status",
                    "creator",
                    "start_date",
                    "deadline_date",
                    "created_at",
                    "updated_at",
                    "deleted_at"
                    )

    list_filter = ("title",
                   "category",
                   "status",
                   "creator",
                   "start_date",
                   "deadline_date",
                   "created_at",
                   "updated_at",
                   "deleted_at"
                   )

    search_fields = ("title", "description")


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    def subtasks_title_to_upper_case(self, request, queryset):
        for obj in queryset:
            obj.title = obj.title.upper()
            obj.save()

    subtasks_title_to_upper_case.short_description = "Title in upper case"

    actions = [
        "subtasks_title_to_upper_case",
    ]

    list_display = ("title", "created_at", "updated_at",)
    list_filter = ("title", "created_at", "updated_at",)
    search_fields = ("title", "created_at", "updated_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at",)
    list_filter = ("name", "created_at", "updated_at",)
    search_fields = ("name", "created_at", "updated_at",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass
