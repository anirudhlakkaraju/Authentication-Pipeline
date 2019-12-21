from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=64, null=True)
    age = models.IntegerField(null=True)
    email = models.CharField(max_length=100, null=True)
    college = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.name}"
