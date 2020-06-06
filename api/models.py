from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Collaborator(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE)