from django.contrib.auth.models import User
from django.db import models


class Applications(models.Model):
    class Meta:
        unique_together = (('owner', 'friend'),)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", null=False, default=None)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", null=False, default=None)
