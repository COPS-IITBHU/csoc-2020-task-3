from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    collaborator=models.ManyToManyField(User,related_name='collaborator')

    def __str__(self):
        return self.title

class Collaborators(models.Model):
    todo=models.ForeignKey(Todo,on_delete=models.CASCADE)
    collaborator=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.collaborator