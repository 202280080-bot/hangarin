from django.db import models


# ============================================================
# BASE MODEL
# ============================================================

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ============================================================
# STATUS CHOICES
# ============================================================

STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("In Progress", "In Progress"),
    ("Completed", "Completed"),
]


# ============================================================
# PRIORITY
# ============================================================

class Priority(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# CATEGORY
# ============================================================

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# TASK
# ============================================================

class Task(BaseModel):
    title = models.CharField(max_length=255)

    description = models.TextField(
        blank=True
    )

    deadline = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    def __str__(self):
        return self.title


# ============================================================
# NOTE
# ============================================================

class Note(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    content = models.TextField()

    def __str__(self):
        return f"Note for {self.task.title}"


# ============================================================
# SUBTASK
# ============================================================

class SubTask(BaseModel):
    parent_task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks"
    )

    title = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    def __str__(self):
        return self.title