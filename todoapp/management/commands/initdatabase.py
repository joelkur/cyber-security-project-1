from django.core.management.base import BaseCommand
from ...models import User, Todo


class Command(BaseCommand):
    help = "Creates test data to database"

    def handle(self, *args, **options):
        users = ["admin", "user1", "user2"]

        for user in users:
            fields = {"username": user, "password": user}
            if user == "admin":
                fields["is_superuser"] = True
                fields["is_staff"] = True
            u = User(**fields)
            u.save()

            for i in range(1, 10):
                todo = Todo(user=u, text=f"{user}'s todo {i}")
                todo.save()
