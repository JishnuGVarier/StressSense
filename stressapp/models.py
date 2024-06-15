from django.contrib.auth.models import AbstractUser
from django.db import models

class Recommendation(models.Model):
    stress_level = models.IntegerField()
    recommend = models.TextField()
