from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    choices = [('GBP','GBP'), ('EUR','EUR'), ('USD','USD'), ('MXN','MXN'), ('AUD','AUD'), ('JPY','JPY')]
    name = models.CharField(max_length=40)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    currency = models.CharField(max_length=24, choices=choices, default="GBP")
    pfp = models.ImageField(upload_to='media/images/pfp', blank=True)
    banner = models.ImageField(upload_to='media/images/banner', blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username

class Bet(models.Model):
    username = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    game = models.CharField(max_length=20)
    amount = models.FloatField()
    date = models.DateField()