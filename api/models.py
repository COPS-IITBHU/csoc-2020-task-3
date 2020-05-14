from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Creator")
    title = models.CharField(max_length=255)
    Collaborators = models.ManyToManyField(User, related_name="Collaborators")
    iscollaborator = models.BooleanField(default=False)
    iscreator = models.BooleanField(default=False)

    def __str__(self):
        return self.title

