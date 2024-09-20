# Generated by Django 5.0.4 on 2024-05-11 12:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_userinfo_selection_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['performance', '-parity'], 'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='selection_date',
            field=models.DateField(blank=True, null=True, verbose_name='Отбор по сроку'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='selection_key',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Отбор по ключу'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['performance', '-parity'], name='tasks_task_perform_390694_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['-parity', 'performance'], name='tasks_task_parity_d32882_idx'),
        ),
    ]
