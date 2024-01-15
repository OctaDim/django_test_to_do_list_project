# Generated by Django 5.0 on 2024-01-15 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0023_subtask_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='note',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='deadline_date',
            field=models.DateField(help_text='Day, when the task should be finished'),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='start_date',
            field=models.DateField(help_text='Day, when the task should be started'),
        ),
    ]
