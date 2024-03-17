from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest

from Corruption_Cove.games.game import Game

class Slots(Game):
    def __init__(self, state, user):
        super().__init__(state,user)
        self.set_state(state)
        self.name = 'slots'

@login_required
def slots(request):
    if request.method == 'POST':
        return JsonResponse()
    else:
        return HttpResponseBadRequest()