from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profiles/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class EmailSubscription(models.Model):
    email = models.EmailField(unique=True)
    consent = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Abonare Email"
        verbose_name_plural = "Abonări Email"