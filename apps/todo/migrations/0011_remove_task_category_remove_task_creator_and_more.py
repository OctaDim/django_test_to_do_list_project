# Generated by Django 5.0 on 2024-01-03 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0010_alter_task_category_alter_task_creator_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
        migrations.RemoveField(
            model_name='task',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='task',
            name='status',
        ),
    ]