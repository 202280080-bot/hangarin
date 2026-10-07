from django.contrib import admin
from django.urls import path
from core_collection import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Tasks
    path("dashboard/task/add/", views.add_task, name="add_task"),
    path("dashboard/task/<int:task_id>/edit/", views.edit_task, name="edit_task"),
    path("dashboard/task/<int:task_id>/delete/", views.delete_task, name="delete_task"),

    # Subtasks
    path("dashboard/subtask/add/", views.add_subtask, name="add_subtask"),
    path("dashboard/subtask/<int:subtask_id>/edit/", views.edit_subtask, name="edit_subtask"),
    path("dashboard/subtask/<int:subtask_id>/delete/", views.delete_subtask, name="delete_subtask"),

    # Notes
    path("dashboard/note/add/", views.add_note, name="add_note"),
    path("dashboard/note/<int:note_id>/edit/", views.edit_note, name="edit_note"),
    path("dashboard/note/<int:note_id>/delete/", views.delete_note, name="delete_note"),

    # Categories
    path("dashboard/category/add/", views.add_category, name="add_category"),
    path("dashboard/category/<int:category_id>/edit/", views.edit_category, name="edit_category"),
    path("dashboard/category/<int:category_id>/delete/", views.delete_category, name="delete_category"),

    # Priorities
    path("dashboard/priority/add/", views.add_priority, name="add_priority"),
    path("dashboard/priority/<int:priority_id>/edit/", views.edit_priority, name="edit_priority"),
    path("dashboard/priority/<int:priority_id>/delete/", views.delete_priority, name="delete_priority"),
]
