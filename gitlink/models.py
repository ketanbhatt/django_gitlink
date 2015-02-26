from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    github_user_name = models.CharField(max_length=256, null=True)
    access = models.CharField(max_length=256, null=True)
    selected_repo = models.CharField(max_length=512, default='')
    user_github_id = models.CharField(max_length=128, null=True)

    def __unicode__(self):
        return self.user.username

class Payload(models.Model):
    for_user = models.ForeignKey(UserProfile)
    message = models.CharField(max_length=1024, null=True)
    url = models.URLField(null=True)

