# Generated by Django 3.2.4 on 2021-07-01 07:49

import apps.core.system
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_task_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='output',
            field=models.FileField(blank=True, max_length=512, upload_to=apps.core.system.get_upload_to),
        ),
    ]