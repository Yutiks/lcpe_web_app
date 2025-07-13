from django.conf import settings
from django.db import models


class TrainingSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    completion = models.TextField(
        blank=True,
        help_text="Example: 'Complete all sets before completing next exercise. Rest between sets: 5–7 min.'"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
