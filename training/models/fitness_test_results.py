from django.db import models
from django.conf import settings


class FitnessTestResult(models.Model):
    RESULT_TYPE_CHOICES = [
        ('initial', 'Initial'),
        ('retest', 'Retest'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    component = models.CharField(max_length=100)
    test_name = models.CharField(max_length=100)
    result = models.IntegerField(null=True, blank=True)
    result_type = models.CharField(max_length=10, choices=RESULT_TYPE_CHOICES)
