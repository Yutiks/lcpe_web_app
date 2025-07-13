from django.db import models
from django.conf import settings


class Food(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    description = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    serving_sizes = models.FloatField(default=100, blank=True)

    calories = models.FloatField()  # required
    fat = models.FloatField()  # required
    saturated = models.FloatField(blank=True, null=True)
    polyunsaturated = models.FloatField(blank=True, null=True)
    monounsaturated = models.FloatField(blank=True, null=True)
    trans = models.FloatField(blank=True, null=True)

    cholesterol = models.FloatField(blank=True, null=True)
    salt = models.FloatField(blank=True, null=True)
    sodium = models.FloatField(blank=True, null=True)
    potassium = models.FloatField(blank=True, null=True)

    carbohydrate = models.FloatField()  # required
    dietary_fiber = models.FloatField(blank=True, null=True)
    sugars = models.FloatField(blank=True, null=True)

    protein = models.FloatField()  # required

    vitamin_a = models.FloatField(blank=True, null=True)
    vitamin_c = models.FloatField(blank=True, null=True)
    calcium = models.FloatField(blank=True, null=True)
    iron = models.FloatField(blank=True, null=True)
    magnesium = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.description
