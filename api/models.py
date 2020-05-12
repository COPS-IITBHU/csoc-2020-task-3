from django.db import models
from authentication.models import AddonUser


class Todo(models.Model):
    creator = models.ForeignKey(AddonUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class contributor(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    person = models.ForeignKey(AddonUser, on_delete=models.CASCADE)
