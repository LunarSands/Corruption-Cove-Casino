import json
import random
from json import JSONDecodeError

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest

from Corruption_Cove.games.game import Game

# Every slots bet costs 100 pounds.
SLOTS_BET = 100
# List of all slot elements.
SLOTS_ELEMENTS = ['Cherry', 'Apple', 'Banana', 'Orange', 'Grapes']

class Slots(Game):
    def __init__(self, state, user):
        super().__init__(state,user)
        self.set_state(state)
        self.name = 'slots'
        self.result = None

    def handle_start(self, request):
        print('slots in process')

        request_body = json.loads(request.body)
        action = request_body.get('action')

        print(self.calculate_win_or_loss())

    def client_state(self):
        return {}

    def calculate_win_or_loss(self):
        result1 = random.choice(SLOTS_ELEMENTS)
        result2 = random.choice(SLOTS_ELEMENTS)
        result3 = random.choice(SLOTS_ELEMENTS)

        if result1 == result2 == result3:
            if result1 == 'Cherry':
                # Jackpot
                return SLOTS_BET * 10
            else:
                # Regular
                return SLOTS_BET * 5
        elif result1 == result2 or result1 == result3 or result2 == result3:
            # Partial
            return SLOTS_BET * 1
        else:
            # Loss
            return SLOTS_BET * -1



@login_required
def slots(request):
    if request.method == 'POST':
        slots_game = Slots({},request.user)

        try:
            print('handling slots')
            slots_game.handle_action(request)
            print('handled slots')
        except ValueError as error:
            print(error)
            return HttpResponseBadRequest()
        
        print(slots_game.client_state())
        return JsonResponse(slots_game.client_state())
    else:
        return HttpResponseBadRequest()