from django.contrib.auth.models import User
from django.db import models


class Applications(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", null=False, default=None)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", null=False, default=None)
