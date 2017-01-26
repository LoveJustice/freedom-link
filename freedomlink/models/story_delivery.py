from django.db import models

from story import Story
from donor import Donor

class StoryDelivery(models.Model):
    donor = models.ForeignKey(Donor)
    story = models.ForeignKey(Story)
    date_sent = models.DateTimeField(null=True)
