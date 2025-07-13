from django.utils.translation import gettext_lazy as _
from django.db import models
from food.models import Food


class Recipe(models.Model):

    MEASUREMENT_UNIT = [
        ('servings', _('servings')),
        ('g', _('grams')),
        ('ml', _('milliliters')),
        ('oz', _('ounces')),
        ('fl_oz', _('fluid ounces')),
    ]

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    by_serving_of = models.FloatField(verbose_name=_("By serving of"))
    measurement_unit = models.CharField(max_length=10, choices=MEASUREMENT_UNIT, default='servings', verbose_name=_("Measurement unit"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    ingredients = models.ManyToManyField(Food, related_name='recipes', verbose_name=_("Ingredients"))
    directions = models.TextField(blank=True, null=True, verbose_name=_("Directions"))

    def __str__(self):
        return self.name
