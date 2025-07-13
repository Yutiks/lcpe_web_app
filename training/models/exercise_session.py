from django.db import models
from .training_session import TrainingSession
from django.conf import settings


class Exercise(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=255)
    duration_min = models.PositiveIntegerField()
    calories_burned = models.FloatField()


class ExerciseSession(models.Model):
    training_session = models.ForeignKey(TrainingSession, related_name='exercises', on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    percentage_1rm = models.PositiveIntegerField(
        help_text="Percentage of your 1RM"
    )
