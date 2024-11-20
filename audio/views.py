from django.shortcuts import render
import os
import subprocess
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_audio(request):
    if request.method == "POST" and request.FILES['audio']:
        audio_file = request.FILES['audio']
        fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'uploads'))
        filename = fs.save(audio_file.name, audio_file)
        audio_path = os.path.join(settings.BASE_DIR, 'uploads', filename)

        # Process the audio using Spleeter (this assumes you want to use 2 stems separation)
        output_dir = os.path.join(settings.BASE_DIR, 'outputs', filename.split('.')[0])
        subprocess.run(['spleeter', 'separate', '-p', 'spleeter:2stems', '-o', output_dir, audio_path])

        return JsonResponse({'message': 'File uploaded and processing started.'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def download_audio(request, filename):
    output_file = os.path.join(settings.BASE_DIR, 'outputs', filename, 'vocals.wav')
    if os.path.exists(output_file):
        with open(output_file, 'rb') as file:
            response = JsonResponse(file.read(), safe=False)
            response['Content-Type'] = 'audio/wav'
            response['Content-Disposition'] = f'attachment; filename={filename}_vocals.wav'
            return response
    return JsonResponse({'error': 'File not found'}, status=404)
