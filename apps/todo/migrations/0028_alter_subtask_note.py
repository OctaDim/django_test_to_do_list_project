# Generated by Django 5.0 on 2024-01-17 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0027_alter_subtask_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='note',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]