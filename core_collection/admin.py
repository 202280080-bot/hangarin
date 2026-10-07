from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Task, SubTask, Category, Priority, Note


def edit_button(obj):
    url = reverse(
        f"admin:core_collection_{obj._meta.model_name}_change",
        args=[obj.pk]
    )
    return format_html('<a href="{}">Edit</a>', url)


def delete_button(obj):
    url = reverse(
        f"admin:core_collection_{obj._meta.model_name}_delete",
        args=[obj.pk]
    )
    return format_html(
        '<a href="{}" style="color:red;">Delete</a>',
        url
    )


edit_button.short_description = "Edit"
delete_button.short_description = "Delete"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "deadline",
        "priority",
        "category",
        edit_button,
        delete_button,
    )

    list_filter = (
        "status",
        "priority",
        "category",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "parent_task_name",
        edit_button,
        delete_button,
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "title",
    )

    def parent_task_name(self, obj):
        return obj.parent_task.title

    parent_task_name.short_description = "Parent Task"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        edit_button,
        delete_button,
    )

    search_fields = (
        "name",
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "content",
        "created_at",
        edit_button,
        delete_button,
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "content",
    )