from django.contrib import admin
from django.contrib.admin import ModelAdmin

from Corruption_Cove.models import UserProfile, Friendship, Bet, Request, Bank
from django.contrib.sessions.models import Session

from Corruption_Cove.models import UserProfile, Friendship, Bet, Request, Bank, Slots, Dealer
from Corruption_Cove.models import *

class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Bet)
admin.site.register(Request)
admin.site.register(Friendship)
admin.site.register(Bank)
admin.site.register(Slots)
admin.site.register(Dealer)
admin.site.register(Deposit)
