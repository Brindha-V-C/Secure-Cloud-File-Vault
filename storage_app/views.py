import queue

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RegisterForm, FileUploadForm
from .models import File
from django.contrib.auth import logout
from django.shortcuts import redirect
from .azure_storage import AzureBlobService
from django.http import HttpResponse
from .queue_service import AzureQueueService

def home(request):
    return redirect("login")


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("files")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def file_list(request):

    files = File.objects.filter(owner=request.user)

    return render(
        request,
        "file_list.html",
        {"files": files},
    )


@login_required
def upload_file(request):
    
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES["file"]
            azure = AzureBlobService()

            blob_name = None

            try:
                # Step 1: Upload to Azure
                blob_name, blob_url = azure.upload_file(uploaded_file)

                # Step 2: Save metadata in DB
                with transaction.atomic():
                    obj = form.save(commit=False)

                    obj.owner = request.user
                    obj.original_filename = uploaded_file.name
                    obj.size = uploaded_file.size
                    obj.content_type = (
                        uploaded_file.content_type
                        or "application/octet-stream"
                    )
                    obj.blob_name = blob_name
                    obj.blob_url = blob_url
                    obj.status = "uploaded"

                    obj.save()

                    queue = AzureQueueService()

                    queue.send_message({
                        "file_id": obj.id,
                        "filename": obj.original_filename,
                        "blob_name": obj.blob_name,
                        "owner": request.user.username,
                        "size": obj.size,
                        "content_type": obj.content_type,
                    })

                return redirect("files")

            except Exception:
                # Compensating cleanup
                if blob_name:
                    try:
                        azure.delete_blob(blob_name)
                    except Exception:
                        # Log this in production
                        pass

                raise

    else:
        form = FileUploadForm()

    return render(request, "upload.html", {"form": form})


@login_required
def download_file(request, pk):

    file = get_object_or_404(
        File,
        pk=pk,
        owner=request.user,
    )

    azure = AzureBlobService()

    file_data = azure.download_blob(file.blob_name)

    response = HttpResponse(
        file_data,
        content_type=file.content_type,
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{file.original_filename}"'
    )

    return response


@login_required
def delete_file(request, pk):

    file = get_object_or_404(
        File,
        pk=pk,
        owner=request.user,
    )

    azure = AzureBlobService()

    azure.delete_blob(file.blob_name)

    file.delete()

    return redirect("files")



def logout_view(request):
    logout(request)
    return redirect("login")