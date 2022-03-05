from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=240)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    urltoken = models.UUIDField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
