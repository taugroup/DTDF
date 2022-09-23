from django.shortcuts import render, get_object_or_404, redirect
import os
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.project.models import Project
from apps.project.models import Project
from apps.file.models import File

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def post(request, project, file_list):
    files = []
    succeed = True

    num_files = len(file_list)

    # only allow two files
    if num_files > settings.PORTAL_MAX_NUMBER_FILES_PER_PROJECT or num_files == 0:
        messages.add_message(request, messages.ERROR,
                             "You can upload up to %s files!" % settings.PORTAL_MAX_NUMBER_FILES_PER_PROJECT)
        succeed = False

    if succeed:
        for f in file_list:
            file_ext = os.path.splitext(f.name)[-1][1:].lower()
            if file_ext != 'json' and file_ext != 'csv':
                messages.add_message(request, messages.ERROR, "Only CVS and JSON files are accepted!")
                return
            try:
                files.append(File(
                    user=request.user,
                    name=os.path.basename(f._name),
                    file=f,
                    folder=project.folder,
                    project=project,
                ))
            except:
                messages.add_message(request, messages.ERROR, "Failed to upload files!")

        File.objects.bulk_create(files)

        messages.add_message(request, messages.SUCCESS, "Upload files successfully!")

#TODO insert virtual sensors
        # for d in File.objects.all():
        #     if not d.text:
        #         d.async_process()
    return


@login_required
def file_create(request, *args, **kwargs):
    project = get_object_or_404(Project, pk=kwargs['pk'])
    filelist = File.objects.filter(project=project)

    context = {
        'file_list': filelist,
        'project': project,
        'max_number_files_per_project': settings.PORTAL_MAX_NUMBER_FILES_PER_PROJECT
    }
    if request.method == 'POST':
        if request.FILES.get("file_list"):
            file_list = request.FILES.getlist("file_list")
            post(request, project, file_list)

    return render(request, 'file/file_form.html', context)

@login_required
def file_delete(request, *args, **kwargs):
    p = get_object_or_404(File, pk=kwargs['pk'])
    project = p.project
    try:
        if p:
            success_message = "File %s was deleted successfully!" % p.name
            messages.success(request, success_message)
            logger.info("File %s was deleted." % p.name)
            p.delete()
    except:
        messages.error(request, "Failed to delete %s!" % p.name)
        pass
    return redirect('file_create', project.id)
