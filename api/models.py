from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

        
class Colloborator(models.Model):
    todo=models.ForeignKey(Todo, null=True,on_delete=models.CASCADE)

    owner=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'by {self.owner.username}'


     