from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def set_password(self, raw_password):
        self.password = raw_password
        self._password = raw_password

    def check_password(self, entered_password):
        return entered_password == self.password

    class Meta:
        db_table = "auth_user"


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    done = models.BooleanField(default=False)
