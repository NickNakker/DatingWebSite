from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biografy = models.TextField(max_length=500, blank=True, null = True)
    location = models.CharField(max_length=50, blank=True, null = True)
    birth_date = models.DateField(null=False, blank=False)
    photo = models.ImageField(upload_to='images', verbose_name='Фото профиля', blank=True, null=True, default='default_avatar.jpg')
    name = models.CharField(max_length=500, blank = True)


    def __str__(self):
        return self.name

class Matching(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like = models.IntegerField(verbose_name ='лайки', null = True, blank = False)
    dislike = models.IntegerField(verbose_name='дизлайки', null = True, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()