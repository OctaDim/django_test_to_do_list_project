# Generated by Django 5.0 on 2024-01-03 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_task_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deleted',
            field=models.BooleanField(),
        ),
    ]
