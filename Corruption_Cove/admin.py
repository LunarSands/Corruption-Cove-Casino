from django.contrib import admin
from Corruption_Cove.models import UserProfile, Friendship, Bet, Request

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Bet)
admin.site.register(Request)
admin.site.register(Friendship)