from django.conf import settings
from django.db import models


class POMSResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    tension_score = models.PositiveSmallIntegerField()
    depression_score = models.PositiveSmallIntegerField()
    anger_score = models.PositiveSmallIntegerField()
    vigor_score = models.PositiveSmallIntegerField()
    fatigue_score = models.PositiveSmallIntegerField()
    confusion_score = models.PositiveSmallIntegerField()
    notes = models.TextField(blank=True)
