from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    choices = [('GBP','GBP'), ('EUR','EUR'), ('USD','USD'), ('MXN','MXN'), ('AUD','AUD'), ('JPY','JPY')]
    name = models.CharField(max_length=40)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    currency = models.CharField(max_length=24, choices=choices, default="GBP")
    pfp = models.ImageField(upload_to='media/images/pfp', blank=True, default="media/images/pfp/default_pfp.png")
    banner = models.ImageField(upload_to='media/images/banner', blank=True, default="media/images/banner/default_banner.png")
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
    slug = models.SlugField(unique=True, default="slug")

    def save(self, num, *args, **kwargs):
        self.slug = slugify(self.username.user.username + str(num))
        super(Bet, self).save(*args, **kwargs)

class Request(models.Model):
    sender = models.ForeignKey(UserProfile, related_name="sender_r", on_delete = models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name="receiver_r",  on_delete = models.CASCADE)
    amount = models.FloatField()

    class Meta:
        unique_together = (('sender', 'receiver'),)

class Friendship(models.Model):
    sender = models.ForeignKey(UserProfile, related_name="sender_f", on_delete = models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name="receiver_f", on_delete = models.CASCADE)

    class Meta:
        unique_together = (('sender', 'receiver'),)

class Bank(models.Model):
    username = models.ForeignKey(UserProfile, related_name="banking", on_delete = models.CASCADE, unique = True)
    balance = models.FloatField()
    name = models.CharField(max_length=40)
    cardNo = models.CharField(max_length=16)
    expiry = models.DateField()
    cvv = models.CharField(max_length=3)
    slug = models.SlugField(unique=True, default="slug")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username.user.username)
        super(Bank, self).save(*args, **kwargs)

class Slots(models.Model):
    theme = models.CharField(max_length=40)
    directory = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.directory = '/media/images/slots/'+self.directory
        super(Slots, self).save(*args, **kwargs)

class Dealer(models.Model):
    name = models.CharField(max_length=20)
    face = models.ImageField()
    stop = models.IntegerField()
    soft = models.BooleanField()

    def save(self, *args, **kwargs):
        self.directory = '/media/images/dealers/'+self.name+'.png'
        super(Dealer, self).save(*args, **kwargs)