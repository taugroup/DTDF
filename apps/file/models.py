import os
from django.db import models
from apps.core.models import CommonInfo
from apps.project.models import Project
from apps.core.system import get_upload_to


class File(CommonInfo):
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_to, blank=True, max_length=512)

    def save(self, *args, **kwargs):
        self.name = self.file.name
        self.folder = self.project.folder

        super(File, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(File, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name
