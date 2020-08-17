from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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

class Projects(models.Model):
    project = models.CharField(max_length = 50)
    project_description = models.CharField(max_length = 1000)
    for_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    repository_link = models.CharField(max_length = 200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project
    
    def save_project(self):
        self.save()
    
    def delete_project(self):
        self.delete()
    
    def update_project(self):
        pass

class Comments(models.Model):
    for_project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    comment = models.CharField(max_length = 500)

    def __str__(self):
        return self.comment

class Review(models.Model):
    for_project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField(auto_now_add=True)
    user_interface = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]) # models.IntegerField(min_value=1, max_value=10)
    user_experience = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]) # models.IntegerField(min_value=1, max_value=10)
    responsiveness = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]) # models.IntegerField(min_value=1, max_value=10)
    design_average = models.IntegerField()
    functionality = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]) # models.IntegerField(min_value=1, max_value=10)
    io = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]) # models.IntegerField(min_value=1, max_value=10)
    usability_average = models.IntegerField()
    content_average = models.IntegerField()
    total_average = models.IntegerField()

    def __str__(self):
        return self.total_average
    
    def save_review(self):
        self.save()
    
    def delete_review(self):
        self.delete()
    
    def update_review(self):
        pass

class Followers(models.Model):
    for_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    follower = models.ManyToManyField(Profile)
    
    def __str__(self):
        return self.follower
    
    def save_follower(self):
        self.save()
    
    def delete_follower(self):
        self.delete()
    
    def update_follower(self):
        pass