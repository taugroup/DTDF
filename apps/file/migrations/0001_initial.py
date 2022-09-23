# Generated by Django 4.1.1 on 2022-09-20 08:32

import apps.core.system
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("project", "0002_alter_project_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("folder", models.CharField(blank=True, max_length=200, null=True)),
                ("time_created", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        max_length=512,
                        upload_to=apps.core.system.get_upload_to,
                    ),
                ),
                ("groups", models.ManyToManyField(blank=True, to="auth.group")),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
