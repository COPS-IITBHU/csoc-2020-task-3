# Generated by Django 3.0.6 on 2020-05-15 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_collaborate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collaborate',
            old_name='todo',
            new_name='title',
        ),
    ]
