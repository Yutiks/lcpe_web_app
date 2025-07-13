from django.conf import settings
from django.db import models


class CSAI2Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    cognitive_score = models.IntegerField()
    somatic_score = models.IntegerField()
    confidence_score = models.IntegerField()
    notes = models.TextField(blank=True)
