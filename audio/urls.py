from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', views.upload_audio, name='upload_audio'),
    path('download/<str:filename>/', views.download_audio, name='download_audio'),
]
