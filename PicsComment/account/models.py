from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    photosCount = models.IntegerField(default=0)
    # store a list of photos for each user - retirve by joining


    def __str__(self):
        return self.user.username

    def clean_photosCount(self):
        count = Photo.objects.all().filter(user = self).count()
        self.photosCount = count



class Photo(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    commentsCount = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    # slug = models.SlugField(null=True, blank=True)
    # list of comments
    def __str__(self):
        return self.name +"_"+ self.user.user.username

    def clean_commentsCount(self):
        count = Comment.objects.all().filter(photo = self).count()
        self.commentsCount=count

    def save(self):
        profile = self.user
        profile.photosCount = profile.photosCount + 1
        profile.save()
        super().save()





class Comment(models.Model):
    photo       = models.ForeignKey(Photo,on_delete=models.CASCADE)
    user        = models.ForeignKey(Profile,on_delete=models.CASCADE)
    text        = models.CharField(max_length=200)
    updated     = models.DateTimeField(auto_now=True,db_index=True)


    def __str__(self):
        return self.photo.name + "_"+ self.user.user.username + "_"+ self.text

    def save(self):
        photo = self.photo
        photo.commentsCount = photo.commentsCount + 1
        photo.updated = timezone.now()
        photo.save()
        super().save()




