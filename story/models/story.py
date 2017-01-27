from django.db import models

from interception_record import InterceptionRecord

class Story(models.Model):
    unique_story_code = models.CharField(max_length=255, unique=True)
    story_text = models.TextField()
    full_name = models.CharField(max_length=255)
    interception_record = models.ForeignKey(InterceptionRecord)