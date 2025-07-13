from django.db import models
from django.conf import settings
from .training_session import TrainingSession


class TrainingPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    current_week = models.PositiveIntegerField(default=1)


class TrainingWeek(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='weeks')
    week_number = models.PositiveIntegerField()

    monday = models.ForeignKey(TrainingSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='monday_sessions')
    monday_time = models.TimeField(null=True, blank=True)

    tuesday = models.ForeignKey(TrainingSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='tuesday_sessions')
    tuesday_time = models.TimeField(null=True, blank=True)

    wednesday = models.ForeignKey(TrainingSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='wednesday_sessions')
    wednesday_time = models.TimeField(null=True, blank=True)

    thursday = models.ForeignKey(TrainingSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='thursday_sessions')
    thursday_time = models.TimeField(null=True, blank=True)

    friday = models.ForeignKey(TrainingSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='friday_sessions')
    friday_time = models.TimeField(null=True, blank=True)

    saturday = models.ForeignKey(TrainingSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='saturday_sessions')
    saturday_time = models.TimeField(null=True, blank=True)

    sunday = models.ForeignKey(TrainingSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='sunday_sessions')
    sunday_time = models.TimeField(null=True, blank=True)


