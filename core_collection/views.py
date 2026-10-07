from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Task, SubTask, Note, Category, Priority


# ============================================================
# LOGIN
# ============================================================

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# ============================================================
# REGISTER
# ============================================================

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not password:
            messages.error(
                request,
                "Please complete all required fields."
            )
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Username already exists."
            )
            return render(request, "register.html")

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(
            request,
            "Account created successfully. You can now log in."
        )

        return redirect("/login/")

    return render(request, "register.html")


# ============================================================
# LOGOUT
# ============================================================

@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("/login/")


# ============================================================
# DASHBOARD
# ============================================================

@login_required(login_url="/login/")
def dashboard(request):
    context = {
        "tasks": Task.objects.all(),
        "subtasks": SubTask.objects.all(),
        "notes": Note.objects.all(),
        "categories": Category.objects.all(),
        "priorities": Priority.objects.all(),

        "task_count": Task.objects.count(),
        "subtask_count": SubTask.objects.count(),
        "note_count": Note.objects.count(),
        "category_count": Category.objects.count(),
        "priority_count": Priority.objects.count(),
    }

    return render(request, "dashboard.html", context)


# ============================================================
# TASKS
# ============================================================

@login_required(login_url="/login/")
def add_task(request):
    categories = Category.objects.all()
    priorities = Priority.objects.all()

    if request.method == "POST":
        Task.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description", ""),
            deadline=request.POST.get("deadline") or None,
            status=request.POST.get("status", "Pending"),
            category_id=request.POST.get("category"),
            priority_id=request.POST.get("priority"),
        )

        return redirect("/dashboard/")

    return render(request, "task_form.html", {
        "categories": categories,
        "priorities": priorities,
    })


@login_required(login_url="/login/")
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description", "")
        task.deadline = request.POST.get("deadline") or None
        task.status = request.POST.get("status", "Pending")
        task.category_id = request.POST.get("category")
        task.priority_id = request.POST.get("priority")

        task.save()

        return redirect("/dashboard/")

    return render(request, "task_form.html", {
        "task": task,
        "categories": Category.objects.all(),
        "priorities": Priority.objects.all(),
    })


@login_required(login_url="/login/")
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.delete()

    return redirect("/dashboard/")


# ============================================================
# SUBTASKS
# ============================================================

@login_required(login_url="/login/")
def add_subtask(request):
    if request.method == "POST":
        SubTask.objects.create(
            parent_task_id=request.POST.get("parent_task"),
            title=request.POST.get("title"),
            status=request.POST.get("status", "Pending"),
        )

        return redirect("/dashboard/")

    return render(request, "subtask_form.html", {
        "tasks": Task.objects.all()
    })


@login_required(login_url="/login/")
def edit_subtask(request, subtask_id):
    subtask = get_object_or_404(
        SubTask,
        id=subtask_id
    )

    if request.method == "POST":
        subtask.parent_task_id = request.POST.get(
            "parent_task"
        )

        subtask.title = request.POST.get("title")

        subtask.status = request.POST.get(
            "status",
            "Pending"
        )

        subtask.save()

        return redirect("/dashboard/")

    return render(request, "subtask_form.html", {
        "subtask": subtask,
        "tasks": Task.objects.all(),
    })


@login_required(login_url="/login/")
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(
        SubTask,
        id=subtask_id
    )

    subtask.delete()

    return redirect("/dashboard/")


# ============================================================
# NOTES
# ============================================================

@login_required(login_url="/login/")
def add_note(request):
    if request.method == "POST":
        Note.objects.create(
            task_id=request.POST.get("task"),
            content=request.POST.get("content", ""),
        )

        return redirect("/dashboard/")

    return render(request, "note_form.html", {
        "tasks": Task.objects.all()
    })


@login_required(login_url="/login/")
def edit_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id
    )

    if request.method == "POST":
        note.task_id = request.POST.get("task")
        note.content = request.POST.get("content", "")

        note.save()

        return redirect("/dashboard/")

    return render(request, "note_form.html", {
        "note": note,
        "tasks": Task.objects.all(),
    })


@login_required(login_url="/login/")
def delete_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id
    )

    note.delete()

    return redirect("/dashboard/")


# ============================================================
# CATEGORIES
# ============================================================

@login_required(login_url="/login/")
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if name:
            Category.objects.create(name=name)

        return redirect("/dashboard/")

    return render(request, "category_form.html")


@login_required(login_url="/login/")
def edit_category(request, category_id):
    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == "POST":
        category.name = request.POST.get(
            "name",
            ""
        ).strip()

        category.save()

        return redirect("/dashboard/")

    return render(request, "category_form.html", {
        "category": category
    })


@login_required(login_url="/login/")
def delete_category(request, category_id):
    category = get_object_or_404(
        Category,
        id=category_id
    )

    category.delete()

    return redirect("/dashboard/")


# ============================================================
# PRIORITIES
# ============================================================

@login_required(login_url="/login/")
def add_priority(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if name:
            Priority.objects.create(name=name)

        return redirect("/dashboard/")

    return render(request, "priority_form.html")


@login_required(login_url="/login/")
def edit_priority(request, priority_id):
    priority = get_object_or_404(
        Priority,
        id=priority_id
    )

    if request.method == "POST":
        priority.name = request.POST.get(
            "name",
            ""
        ).strip()

        priority.save()

        return redirect("/dashboard/")

    return render(request, "priority_form.html", {
        "priority": priority
    })


@login_required(login_url="/login/")
def delete_priority(request, priority_id):
    priority = get_object_or_404(
        Priority,
        id=priority_id
    )

    priority.delete()

    return redirect("/dashboard/")
