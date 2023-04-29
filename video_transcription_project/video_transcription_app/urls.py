from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('video-processed/',views.transcribe_video,name="transcribe_video"),
]
