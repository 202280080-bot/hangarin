from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import Task, SubTask, Note, Category, Priority


# ============================================================
# LOGIN
# ============================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "login.html")


# ============================================================
# REGISTER
# ============================================================

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not email or not password:
            return render(
                request,
                "register.html",
                {"error": "Please fill in all fields."}
            )

        if password != confirm_password:
            return render(
                request,
                "register.html",
                {"error": "Passwords do not match."}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "register.html",
                {"error": "Username already exists."}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("dashboard")

    return render(request, "register.html")


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):
    tasks = Task.objects.select_related(
        "category",
        "priority"
    ).order_by("-created_at")

    subtasks = SubTask.objects.select_related(
        "parent_task"
    ).order_by("-created_at")

    notes = Note.objects.select_related(
        "task"
    ).order_by("-created_at")

    categories = Category.objects.all()
    priorities = Priority.objects.all()

    context = {
        "tasks": tasks,
        "subtasks": subtasks,
        "notes": notes,
        "categories": categories,
        "priorities": priorities,

        "task_count": tasks.count(),
        "subtask_count": subtasks.count(),
        "note_count": notes.count(),
        "category_count": categories.count(),
        "priority_count": priorities.count(),
    }

    return render(request, "dashboard.html", context)


# ============================================================
# TASKS
# ============================================================

@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")
        status = request.POST.get("status")
        category_id = request.POST.get("category")
        priority_id = request.POST.get("priority")

        if title and category_id and priority_id:
            Task.objects.create(
                title=title,
                description=description,
                deadline=deadline if deadline else None,
                status=status or "Pending",
                category_id=category_id,
                priority_id=priority_id,
            )

    return redirect("dashboard")


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.deadline = request.POST.get("deadline") or None
        task.status = request.POST.get("status")
        task.category_id = request.POST.get("category")
        task.priority_id = request.POST.get("priority")
        task.save()

    return redirect("dashboard")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()

    return redirect("dashboard")


# ============================================================
# SUBTASKS
# ============================================================

@login_required
def add_subtask(request):
    if request.method == "POST":
        title = request.POST.get("title")
        parent_task_id = request.POST.get("parent_task")
        status = request.POST.get("status")

        if title and parent_task_id:
            SubTask.objects.create(
                title=title,
                parent_task_id=parent_task_id,
                status=status or "Pending",
            )

    return redirect("dashboard")


@login_required
def edit_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    if request.method == "POST":
        subtask.title = request.POST.get("title")
        subtask.parent_task_id = request.POST.get("parent_task")
        subtask.status = request.POST.get("status")
        subtask.save()

    return redirect("dashboard")


@login_required
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    if request.method == "POST":
        subtask.delete()

    return redirect("dashboard")


# ============================================================
# NOTES
# ============================================================

@login_required
def add_note(request):
    if request.method == "POST":
        task_id = request.POST.get("task")
        content = request.POST.get("content")

        if task_id and content:
            Note.objects.create(
                task_id=task_id,
                content=content,
            )

    return redirect("dashboard")


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":
        note.task_id = request.POST.get("task")
        note.content = request.POST.get("content")
        note.save()

    return redirect("dashboard")


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":
        note.delete()

    return redirect("dashboard")


# ============================================================
# CATEGORIES
# ============================================================

@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            Category.objects.get_or_create(name=name)

    return redirect("dashboard")


@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            category.name = name
            category.save()

    return redirect("dashboard")


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.delete()

    return redirect("dashboard")


# ============================================================
# PRIORITIES
# ============================================================

@login_required
def add_priority(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            Priority.objects.get_or_create(name=name)

    return redirect("dashboard")


@login_required
def edit_priority(request, priority_id):
    priority = get_object_or_404(Priority, id=priority_id)

    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            priority.name = name
            priority.save()

    return redirect("dashboard")


@login_required
def delete_priority(request, priority_id):
    priority = get_object_or_404(Priority, id=priority_id)

    if request.method == "POST":
        priority.delete()

    return redirect("dashboard")


# ============================================================
# LOGOUT
# ============================================================

def logout_view(request):
    logout(request)
    return redirect("login")
