# Generated by Django 5.0 on 2024-01-17 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0025_alter_subtask_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='todo.task'),
        ),
    ]