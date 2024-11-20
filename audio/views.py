from django.shortcuts import render
import os
import subprocess
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def upload_audio(request):
    return HttpResponse("Welcome to the Audio Processing App!")


def download_audio(request, filename):
    output_file = os.path.join(settings.BASE_DIR, 'outputs', filename, 'vocals.wav')
    if os.path.exists(output_file):
        with open(output_file, 'rb') as file:
            response = JsonResponse(file.read(), safe=False)
            response['Content-Type'] = 'audio/wav'
            response['Content-Disposition'] = f'attachment; filename={filename}_vocals.wav'
            return response
    return JsonResponse({'error': 'File not found'}, status=404)
