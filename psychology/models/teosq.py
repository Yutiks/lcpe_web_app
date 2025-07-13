from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TEOSQResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    task_orientation = models.PositiveSmallIntegerField(verbose_name=_("Task Orientation (Out of 5)"))
    ego_orientation = models.PositiveSmallIntegerField(verbose_name=_("Ego Orientation (Out of 5)"))
    dominant_type = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
