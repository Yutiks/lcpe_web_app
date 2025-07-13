from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class SCATResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    score = models.PositiveSmallIntegerField(verbose_name=_("SCAT Score (Out of 30)"))
    interpretation = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
