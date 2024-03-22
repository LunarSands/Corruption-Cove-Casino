from django.shortcuts import redirect
from django.urls import reverse

from Corruption_Cove.models import Bank, UserProfile


def card_required(function):
    def wrapper(request, *args, **kwargs):
        user = request.user
        user_prof = UserProfile.objects.get(user=user)
        try:
            card = Bank.objects.get(username=user_prof)
        except Bank.DoesNotExist:
            return redirect(reverse('corruption-cove-casino:add_card',kwargs={'user_slug':user_prof.slug}))
        return function(request, *args, **kwargs)

    return wrapper
