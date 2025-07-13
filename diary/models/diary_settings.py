from django.conf import settings
from django.db import models


class DiarySettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diary')

    show_water_tracker = models.BooleanField(default=True)
    show_exercise_tracker = models.BooleanField(default=True)
    show_meals_time = models.BooleanField(default=False)
