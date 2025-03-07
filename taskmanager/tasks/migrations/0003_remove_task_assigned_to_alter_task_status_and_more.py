# Generated by Django 5.1.3 on 2024-11-16 11:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_task_assigned_to_alter_task_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_to',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ManyToManyField(related_name='assigned_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
