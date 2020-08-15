from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, default=0000, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.EmailField()
    bio = models.TextField()
    phone_number = models.CharField(max_length =15, blank = True)
    prof_photo = models.ImageField(upload_to = 'pics/profiles/')

    def __str__(self):
        return self.first_name
    
    def save_profile(self):
        self.save()
    
    def delete_profile(self):
        self.delete()
    
    def update_profile(self):
        pass
    
    
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(self, sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(self, sender, instance, **kwargs):
        instance.profile.save()

class Comments(models.Model):
    for_comment = models.IntegerField()
    comment = models.CharField(max_length = 500)

    def __str__(self):
        return self.comment

class Projects(models.Model):
    pass
