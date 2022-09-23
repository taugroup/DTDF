# Generated by Django 3.2.5 on 2021-07-04 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_task_output'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('running', 'Running'), ('queued', 'Queued'), ('finished', 'Finished')], default='queued', max_length=10),
        ),
    ]