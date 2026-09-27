from django.shortcuts import render
from .models import Task, Note, SubTask, Priority, Category


def home(request):
    context = {
        "tasks": Task.objects.select_related("priority", "category").order_by("deadline")[:8],
        "task_count": Task.objects.count(),
        "note_count": Note.objects.count(),
        "subtask_count": SubTask.objects.count(),
        "priority_count": Priority.objects.count(),
        "category_count": Category.objects.count(),
    }

    return render(request, "core_collection/home.html", context)
