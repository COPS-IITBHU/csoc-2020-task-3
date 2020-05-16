from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    collaborators = JSONField(default = [], blank = True, null = True)

    def __str__(self):
        return self.title