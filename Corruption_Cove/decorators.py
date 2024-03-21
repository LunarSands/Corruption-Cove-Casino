from django.shortcuts import redirect
from django.urls import reverse

from Corruption_Cove.models import Bank, UserProfile


def card_required(function):
    def wrapper(request, *args, **kwargs):
        user = request.user
        user_prof = UserProfile.objects.get(user=user)
        card = Bank.objects.get(username=user_prof)
        if card is None:
            return redirect(reverse('corruption-cove-casino:account') + f'/{user_prof.slug}')
        return function(request, *args, **kwargs)

    return wrapper
