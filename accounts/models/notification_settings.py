from django.db import models
from django.conf import settings


class UserNotificationSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    notify_training_reminder = models.BooleanField(default=True)
    notify_week_completion = models.BooleanField(default=True)

    email_notifications = models.BooleanField(default=True)
    site_notifications = models.BooleanField(default=True)

    reminder_lead_time = models.IntegerField(
        choices=[
            (5, "5 minutes"),
            (10, "10 minutes"),
            (15, "15 minutes"),
            (30, "30 minutes"),
        ],
        default=10
    )

