# Generated by Django 5.0 on 2024-01-12 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0019_remove_task_test_blank_field_task_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='note',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
