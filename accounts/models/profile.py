from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    ACTIVITY_LEVEL_CHOICES = [
        ('low', 'Low - Little or no exercise'),
        ('moderate', 'Moderate - Light exercise, 1–3 times/week'),
        ('high', 'High - Moderate exercise, 3–5 times/week'),
        ('very_high', 'Very high - Intense exercise, 6–7 days/week'),
        ('hyperactive', 'Hyperactive - Very intense, 2h+ per day'),
    ]

    GOAL_CHOICES = [
        ('lose_20', 'Lose weight - 20%'),
        ('lose_10', 'Lose weight slowly - 10%'),
        ('maintain', 'Maintain weight'),
        ('gain_10', 'Gain weight slowly - 10%'),
        ('gain_20', 'Gain weight - 20%'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    height_cm = models.PositiveIntegerField(default=175)
    weight_kg = models.FloatField(default=65.0)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    age = models.PositiveIntegerField(default=18)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, default='moderate')
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='maintain')
    fat_percentage = models.FloatField(null=True, blank=True)
