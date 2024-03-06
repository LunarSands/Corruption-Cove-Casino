from django.contrib import admin
from Corruption_Cove.models import UserProfile, Friendship, Bet, Request, Bank, Slots, Dealer

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Bet)
admin.site.register(Request)
admin.site.register(Friendship)
admin.site.register(Bank)
admin.site.register(Slots)
admin.site.register(Dealer)
