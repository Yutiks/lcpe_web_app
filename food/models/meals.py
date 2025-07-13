from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Meal(models.Model):
    """
    Названия приёмов пищи, настроенные пользователем (например: Завтрак, Обед, Ужин).
    """
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meals')

    class Meta:
        unique_together = ('name', 'user')


class MealItem(models.Model):
    meal_entry = models.ForeignKey("MealEntry", on_delete=models.CASCADE, related_name="items")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    food_or_recipe = GenericForeignKey('content_type', 'object_id')
    amount = models.FloatField(default=1.0)


class MealEntry(models.Model):
    """
     Конкретный приём пищи в конкретный день: содержит привязку к Meal, время и еду.
     """
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='entries')
    time = models.TimeField(null=True)
