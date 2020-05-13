from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    ##-- Todo Model --##
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # Each todo can have many collaborators and each user can collaborate on many todos
    # So we chose ManytoManyField
    collaborator = models.ManyToManyField(User, related_name='collaborator')

    def __str__(self):
        return self.title