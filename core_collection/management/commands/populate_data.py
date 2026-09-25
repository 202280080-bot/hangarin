from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker

from core_collection.models import (
    Task,
    Note,
    SubTask,
    Priority,
    Category,
)


class Command(BaseCommand):
    help = "Populate Task, Note, and SubTask with fake data."

    def handle(self, *args, **options):
        fake = Faker()

        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        if not priorities:
            raise CommandError(
                "No Priority records found. Add the required Priority "
                "records first: high, medium, low, critical, optional."
            )

        if not categories:
            raise CommandError(
                "No Category records found. Add the required Category "
                "records first: Work, School, Personal, Finance, Projects."
            )

        statuses = [
            "Pending",
            "In Progress",
            "Completed",
        ]

        tasks = []

        # Create 10 fake Tasks
        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(
                    fake.date_time_this_month()
                ),
                status=fake.random_element(elements=statuses),
                priority=fake.random_element(elements=priorities),
                category=fake.random_element(elements=categories),
            )

            tasks.append(task)

        # Create 20 fake Notes
        for _ in range(20):
            task = fake.random_element(elements=tasks)

            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=3),
            )

        # Create 20 fake SubTasks
        for _ in range(20):
            task = fake.random_element(elements=tasks)

            SubTask.objects.create(
                parent_task=task,
                title=fake.sentence(nb_words=5),
                status=fake.random_element(elements=statuses),
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created 10 Tasks, 20 Notes, and 20 SubTasks."
            )
        )