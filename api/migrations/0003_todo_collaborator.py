# Generated by Django 3.0.6 on 2020-05-13 07:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_todo_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='collaborator',
            field=models.ManyToManyField(related_name='collaborator', to=settings.AUTH_USER_MODEL),
        ),
    ]
