from django.db import models

# Create your models here.
#video models
class Video(models.Model):
    video_url=models.URLField(max_length=500)
    transcript=models.TextField()
    
    def __str__(self):
        return self.video_url
