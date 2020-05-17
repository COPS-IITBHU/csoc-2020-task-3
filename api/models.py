from django.db import models
from django.contrib.auth.models import User




class Todo(models.Model):
    creator = models.ForeignKey(User,related_name='creator', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    collaborators = models.ManyToManyField(User,related_name='collaborators')

    def __str__(self):
        return self.title