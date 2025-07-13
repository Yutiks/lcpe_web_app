from django.conf import settings
from django.db import models
from training.models.exercise_session import Exercise
from food.models import MealEntry


class DailyLog(models.Model):
    """
    Дневниковая запись за один день. Хранит приёмы пищи, упражнения и воду.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField()
    meals = models.ManyToManyField(MealEntry, blank=True, related_name='daily_logs')
    exercises = models.ManyToManyField(Exercise, blank=True, related_name='daily_logs')
    water_intake_ml = models.PositiveIntegerField(default=0)
