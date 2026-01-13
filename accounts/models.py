from django.db import models                    #creates tables
from django.contrib.auth.models import User     #Django model for users
from django.db.models.signals import post_save  #Singal which will be sent when an object is added to the DataBase
from django.dispatch import receiver            #Decorator for connecting signal with function

# Create your models here

class Profile(models.Model):
    """ Creating profile model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    #automatically creating profile when a user is created
    @receiver(post_save, sender=User) # This decorator is listening for an event
    def create_user_profile(sender, instance, created, **kwargs):
        if created:     # check if the user was just created and not just edited
            Profile.objects.create(user=instance) # create new profile

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        #Checks if the profile exists before trying to save it
        if hasattr(instance, 'user'):
            instance.profile.save()


