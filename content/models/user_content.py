from django.conf import settings
from django.db import models
from food.models import Food, Recipe
from training.models.exercise_session import Exercise


class UserContent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_content')
    my_foods = models.ManyToManyField(Food, blank=True, related_name='created_by_users')
    my_exercises = models.ManyToManyField(Exercise, blank=True, related_name='created_by_users')
    my_recipes = models.ManyToManyField(Recipe, blank=True, related_name='created_by_users')
