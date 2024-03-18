import json
import random
from json import JSONDecodeError

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest

from Corruption_Cove.games.game import Game

class Slots(Game):
    def __init__(self, state, user):
        super().__init__(state,user)
        self.set_state(state)
        self.name = 'slots'

    def handle_start(self, action):
        print('slots in process')

    def client_state(self):
        return {}


@login_required
def slots(request):
    if request.method == 'POST':
        slots_game = Slots({},request.user)

        try:
            action = json.loads(request.body)
            print('handling slots')
            slots_game.handle_action(action)
            print('handled slots')
        except ValueError as error:
            print(error)
            return HttpResponseBadRequest()
        
        print(slots_game.client_state())
        return JsonResponse(slots_game.client_state())
    else:
        return HttpResponseBadRequest()
