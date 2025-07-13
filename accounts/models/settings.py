from django.db import models
from django.conf import settings


class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    HEIGHT_UNITS = [('cm', 'Centimeters'), ('ft_in', 'Feet and inches')]
    WEIGHT_UNITS = [('kg', 'Kilograms'), ('lbs', 'Pounds')]
    ENERGY_UNITS = [('kcal', 'Calories'), ('kj', 'Kilojoules')]
    WATER_UNITS = [('ml', 'Milliliters'), ('oz', 'Ounces'), ('cups', 'Cups')]

    DATE_FORMATS = [
        ('DD/MM/YYYY', 'DD/MM/YYYY'),
        ('MM/DD/YYYY', 'MM/DD/YYYY'),
        ('YYYY/MM/DD', 'YYYY/MM/DD'),
    ]
    TIME_FORMATS = [('24h', '24 часа'), ('12h', '12 часов')]
    WEEK_STARTS = [('sunday', 'Sunday'), ('monday', 'Monday')]

    FORMULAS = [
        ('harris_benedict', 'Harris-Benedict'),
        ('mifflin_st_jeor', 'Mifflin-St Jeor'),
        ('katch_mcardle', 'Katch-McArdle'),
    ]

    TIMEZONES = [
        ('Europe/Moscow', 'Europe/Moscow'),
        ('Europe/Dublin', 'Europe/Dublin'),
        ('America/New_York', 'America/New_York'),
        ('Asia/Dubai', 'Asia/Dubai'),
        ('Asia/Riyadh', 'Asia/Riyadh'),
    ]

    LANGUAGES = [('en', 'English'), ('ru', 'Русский')]

    DIET_CHOICES = [
        ('standard', 'Standard'),
        ('balanced', 'Balanced'),
        ('low_fat', 'Low fat'),
        ('high_protein', 'High in Protein'),
        ('ketogenic', 'Ketogenic'),
        ('custom', 'Custom')
    ]

    height_unit = models.CharField(max_length=10, choices=HEIGHT_UNITS, default='cm')
    weight_unit = models.CharField(max_length=10, choices=WEIGHT_UNITS, default='kg')
    energy_unit = models.CharField(max_length=10, choices=ENERGY_UNITS, default='kcal')
    water_unit = models.CharField(max_length=10, choices=WATER_UNITS, default='ml')

    date_format = models.CharField(max_length=20, choices=DATE_FORMATS, default='DD/MM/YYYY')
    time_format = models.CharField(max_length=5, choices=TIME_FORMATS, default='24h')
    week_start = models.CharField(max_length=10, choices=WEEK_STARTS, default='monday')

    formula = models.CharField(max_length=20, choices=FORMULAS, default='mifflin_st_jeor')
    timezone = models.CharField(max_length=30, choices=TIMEZONES, default='Europe/Dublin')
    language = models.CharField(max_length=5, choices=LANGUAGES, default='en')
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES, default='standard')
