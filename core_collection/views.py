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
    if request.user.is_authenticated:
        return redirect("/dashboard/")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Please enter your username and password.")
            return render(request, "login.html")

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
    if request.user.is_authenticated:
        return redirect("/dashboard/")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not password or not confirm_password:
            messages.error(request, "Please complete all required fields.")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
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
        "tasks": Task.objects.select_related(
            "category",
            "priority"
        ).all(),

        "subtasks": SubTask.objects.select_related(
            "parent_task"
        ).all(),

        "notes": Note.objects.select_related(
            "task"
        ).all(),

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
# TASK - ADD
# ============================================================

@login_required(login_url="/login/")
def add_task(request):
    categories = Category.objects.all()
    priorities = Priority.objects.all()

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        deadline = request.POST.get("deadline", "").strip()
        status = request.POST.get("status", "Pending").strip()
        category_id = request.POST.get("category", "").strip()
        priority_id = request.POST.get("priority", "").strip()

        # Required title
        if not title:
            messages.error(request, "Task title is required.")

            return render(request, "task_form.html", {
                "categories": categories,
                "priorities": priorities,
            })

        # Required category
        if not category_id:
            messages.error(request, "Please select a category.")

            return render(request, "task_form.html", {
                "categories": categories,
                "priorities": priorities,
            })

        # Required priority
        if not priority_id:
            messages.error(request, "Please select a priority.")

            return render(request, "task_form.html", {
                "categories": categories,
                "priorities": priorities,
            })

        # Make sure category exists
        category = get_object_or_404(
            Category,
            id=category_id
        )

        # Make sure priority exists
        priority = get_object_or_404(
            Priority,
            id=priority_id
        )

        # Validate status
        valid_statuses = [
            "Pending",
            "In Progress",
            "Completed"
        ]

        if status not in valid_statuses:
            status = "Pending"

        # Create task
        Task.objects.create(
            title=title,
            description=description,
            deadline=deadline if deadline else None,
            status=status,
            category=category,
            priority=priority,
        )

        messages.success(
            request,
            "Task added successfully!"
        )

        return redirect("/dashboard/")

    return render(request, "task_form.html", {
        "categories": categories,
        "priorities": priorities,
    })


# ============================================================
# TASK - EDIT
# ============================================================

@login_required(login_url="/login/")
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    categories = Category.objects.all()
    priorities = Priority.objects.all()

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        deadline = request.POST.get("deadline", "").strip()
        status = request.POST.get("status", "Pending").strip()
        category_id = request.POST.get("category", "").strip()
        priority_id = request.POST.get("priority", "").strip()

        if not title:
            messages.error(request, "Task title is required.")

            return render(request, "task_form.html", {
                "task": task,
                "categories": categories,
                "priorities": priorities,
            })

        if not category_id:
            messages.error(request, "Please select a category.")

            return render(request, "task_form.html", {
                "task": task,
                "categories": categories,
                "priorities": priorities,
            })

        if not priority_id:
            messages.error(request, "Please select a priority.")

            return render(request, "task_form.html", {
                "task": task,
                "categories": categories,
                "priorities": priorities,
            })

        category = get_object_or_404(
            Category,
            id=category_id
        )

        priority = get_object_or_404(
            Priority,
            id=priority_id
        )

        valid_statuses = [
            "Pending",
            "In Progress",
            "Completed"
        ]

        if status not in valid_statuses:
            status = "Pending"

        task.title = title
        task.description = description
        task.deadline = deadline if deadline else None
        task.status = status
        task.category = category
        task.priority = priority

        task.save()

        messages.success(
            request,
            "Task updated successfully!"
        )

        return redirect("/dashboard/")

    return render(request, "task_form.html", {
        "task": task,
        "categories": categories,
        "priorities": priorities,
    })


# ============================================================
# TASK - DELETE
# ============================================================

@login_required(login_url="/login/")
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.delete()

    messages.success(
        request,
        "Task deleted successfully!"
    )

    return redirect("/dashboard/")


# ============================================================
# SUBTASK - ADD
# ============================================================

@login_required(login_url="/login/")
def add_subtask(request):
    tasks = Task.objects.all()

    if request.method == "POST":

        parent_task_id = request.POST.get(
            "parent_task",
            ""
        ).strip()

        title = request.POST.get(
            "title",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            "Pending"
        ).strip()

        if not parent_task_id:
            messages.error(
                request,
                "Please select a parent task."
            )

            return render(request, "subtask_form.html", {
                "tasks": tasks
            })

        if not title:
            messages.error(
                request,
                "Subtask title is required."
            )

            return render(request, "subtask_form.html", {
                "tasks": tasks
            })

        parent_task = get_object_or_404(
            Task,
            id=parent_task_id
        )

        valid_statuses = [
            "Pending",
            "In Progress",
            "Completed"
        ]

        if status not in valid_statuses:
            status = "Pending"

        SubTask.objects.create(
            parent_task=parent_task,
            title=title,
            status=status,
        )

        messages.success(
            request,
            "Subtask added successfully!"
        )

        return redirect("/dashboard/")

    return render(request, "subtask_form.html", {
        "tasks": tasks
    })


# ============================================================
# SUBTASK - EDIT
# ============================================================

@login_required(login_url="/login/")
def edit_subtask(request, subtask_id):
    subtask = get_object_or_404(
        SubTask,
        id=subtask_id
    )

    tasks = Task.objects.all()

    if request.method == "POST":

        parent_task_id = request.POST.get(
            "parent_task",
            ""
        ).strip()

        title = request.POST.get(
            "title",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            "Pending"
        ).strip()

        if not parent_task_id:
            messages.error(
                request,
                "Please select a parent task."
            )

            return render(request, "subtask_form.html", {
                "subtask": subtask,
                "tasks": tasks
            })

        if not title:
            messages.error(
                request,
                "Subtask title is required."
            )

            return render(request, "subtask_form.html", {
                "subtask": subtask,
                "tasks": tasks
            })

        parent_task = get_object_or_404(
            Task,
            id=parent_task_id
        )

        valid_statuses = [
            "Pending",
            "In Progress",
            "Completed"
        ]

        if status not in valid_statuses:
            status = "Pending"

        subtask.parent_task = parent_task
        subtask.title = title
        subtask.status = status

        subtask.save()

        messages.success(
            request,
            "Subtask updated successfully!"
        )

        return redirect("/dashboard/")

    return render(request, "subtask_form.html", {
        "subtask": subtask,
        "tasks": tasks,
    })


# ============================================================
# SUBTASK - DELETE
# ============================================================

@login_required(login_url="/login/")
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(
        SubTask,
        id=subtask_id
    )

    subtask.delete()

    messages.success(
        request,
        "Subtask deleted successfully!"
    )

    return redirect("/dashboard/")


# ============================================================
# NOTE - ADD
# ============================================================

@login_required(login_url="/login/")
def add_note(request):
    tasks = Task.objects.all()

    if request.method == "POST":

        task_id = request.POST.get(
            "task",
            ""
        ).strip()

        content = request.POST.get(
            "content",
            ""
        ).strip()

        if not task_id:
            messages.error(
                request,
                "Please select a task."
            )

            return render(request, "note_form.html", {
                "tasks": tasks
            })

        if not content:
            messages.error(
                request,
                "Note content is required."
            )

            return render(request, "note_form.html", {
                "tasks": tasks
            })

        task = get_object_or_404(
            Task,
            id=task_id
        )

        Note.objects.create(
            task=task,
            content=content,
        )

        messages.success(
            request,
            "Note added successfully!"
        )

        return redirect("/dashboard/")

    return render(request, "note_form.html", {
        "tasks": tasks
    })


# ============================================================
# NOTE - EDIT
# ============================================================

@login_required(login_url="/login/")
def edit_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id
    )

    tasks = Task.objects.all()

    if request.method == "POST":

        task_id = request.POST.get(
            "task",
            ""
        ).strip()

        content = request.POST.get(
            "content",
            ""
        ).strip()

        if not task_id:
            messages.error(
                request,
                "Please select a task."
            )

            return render(request, "note_form.html", {
                "note": note,
                "tasks": tasks
            })

        if not content:
            messages.error(
                request,
                "Note content is required."
            )

            return render(request, "note_form.html", {
                "note": note,
                "tasks": tasks
            })

        task = get_object_or_404(
            Task,
            id=task_id
        )

        note.task = task
        note.content = content

        note.save()

        messages.success(
            request,
            "Note updated successfully!"
        )

        return redirect("/dashboard/")

    return render(request, "note_form.html", {
        "note": note,
        "tasks": tasks,
    })


# ============================================================
# NOTE - DELETE
# ============================================================

@login_required(login_url="/login/")
def delete_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id
    )

    note.delete()

    messages.success(
        request,
        "Note deleted successfully!"
    )

    return redirect("/dashboard/")


# ============================================================
# CATEGORY - ADD
# ============================================================

@login_required(login_url="/login/")
def add_category(request):
    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        if not name:
            messages.error(
                request,
                "Category name is required."
            )

            return render(
                request,
                "category_form.html"
            )

        if Category.objects.filter(
            name__iexact=name
        ).exists():

            messages.error(
                request,
                "This category already exists."
            )

            return render(
                request,
                "category_form.html"
            )

        Category.objects.create(
            name=name
        )

        messages.success(
            request,
            "Category added successfully!"
        )

        return redirect("/dashboard/")

    return render(
        request,
        "category_form.html"
    )


# ============================================================
# CATEGORY - EDIT
# ============================================================

@login_required(login_url="/login/")
def edit_category(request, category_id):
    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        if not name:
            messages.error(
                request,
                "Category name is required."
            )

            return render(
                request,
                "category_form.html",
                {"category": category}
            )

        duplicate = Category.objects.filter(
            name__iexact=name
        ).exclude(
            id=category.id
        ).exists()

        if duplicate:
            messages.error(
                request,
                "This category already exists."
            )

            return render(
                request,
                "category_form.html",
                {"category": category}
            )

        category.name = name
        category.save()

        messages.success(
            request,
            "Category updated successfully!"
        )

        return redirect("/dashboard/")

    return render(
        request,
        "category_form.html",
        {"category": category}
    )


# ============================================================
# CATEGORY - DELETE
# ============================================================

@login_required(login_url="/login/")
def delete_category(request, category_id):
    category = get_object_or_404(
        Category,
        id=category_id
    )

    category.delete()

    messages.success(
        request,
        "Category deleted successfully!"
    )

    return redirect("/dashboard/")


# ============================================================
# PRIORITY - ADD
# ============================================================

@login_required(login_url="/login/")
def add_priority(request):
    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        if not name:
            messages.error(
                request,
                "Priority name is required."
            )

            return render(
                request,
                "priority_form.html"
            )

        if Priority.objects.filter(
            name__iexact=name
        ).exists():

            messages.error(
                request,
                "This priority already exists."
            )

            return render(
                request,
                "priority_form.html"
            )

        Priority.objects.create(
            name=name
        )

        messages.success(
            request,
            "Priority added successfully!"
        )

        return redirect("/dashboard/")

    return render(
        request,
        "priority_form.html"
    )


# ============================================================
# PRIORITY - EDIT
# ============================================================

@login_required(login_url="/login/")
def edit_priority(request, priority_id):
    priority = get_object_or_404(
        Priority,
        id=priority_id
    )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        if not name:
            messages.error(
                request,
                "Priority name is required."
            )

            return render(
                request,
                "priority_form.html",
                {"priority": priority}
            )

        duplicate = Priority.objects.filter(
            name__iexact=name
        ).exclude(
            id=priority.id
        ).exists()

        if duplicate:
            messages.error(
                request,
                "This priority already exists."
            )

            return render(
                request,
                "priority_form.html",
                {"priority": priority}
            )

        priority.name = name
        priority.save()

        messages.success(
            request,
            "Priority updated successfully!"
        )

        return redirect("/dashboard/")

    return render(
        request,
        "priority_form.html",
        {"priority": priority}
    )


# ============================================================
# PRIORITY - DELETE
# ============================================================

@login_required(login_url="/login/")
def delete_priority(request, priority_id):
    priority = get_object_or_404(
        Priority,
        id=priority_id
    )

    priority.delete()

    messages.success(
        request,
        "Priority deleted successfully!"
    )

    return redirect("/dashboard/")