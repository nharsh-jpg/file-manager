from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import FileItem


def home(request):
    files = FileItem.objects.all().order_by("-uploaded_at")
    return render(request, "filemanager/index.html", {"files": files})


@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return JsonResponse(
                {"error": "No file selected"},
                status=400
            )

        file_item = FileItem.objects.create(
            name=uploaded_file.name,
            file=uploaded_file
        )

        return JsonResponse({
            "message": "File uploaded successfully",
            "id": file_item.id,
            "name": file_item.name
        })

    return JsonResponse(
        {"error": "POST request required"},
        status=405
    )


def file_list(request):
    files = FileItem.objects.all().order_by("-uploaded_at")

    data = []

    for item in files:
        data.append({
            "id": item.id,
            "name": item.name,
            "url": item.file.url,
            "uploaded_at": item.uploaded_at
        })

    return JsonResponse(data, safe=False)