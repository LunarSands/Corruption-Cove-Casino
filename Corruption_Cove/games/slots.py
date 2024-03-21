import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest

from Corruption_Cove.games.game import Game
from Corruption_Cove.models import Bank, Bet, UserProfile

# Every slots bet costs 100 pounds.
SLOTS_BET = 100
# List of all slot elements.
SLOTS_ELEMENTS = ['1', '2', '3', '4', '5']
# Multiplicators for different spin outcomes.
SPIN_MULTIPLICATORS = {'jackpot': 10, 'regular': 5, 'partial': 2, 'loss': 0}

class Slots(Game):
    def __init__(self, state, user):
        super().__init__(state,user)

        self.name = 'slots'
        self.spin_results = []
        self.spin_amount_result = 0

    def handle_start(self, action):
        self.spin_amount_result, self.spin_results = self.spin_slots()

        net_winnings= self.spin_amount_result - SLOTS_BET
        # If error occurs, comment out the line below and debug the add_bet func.
        self.add_bet_results(net_winnings)

    def client_state(self):
        return {'spin_result': self.spin_results,'spin_amount': self.spin_amount_result}

    def spin_slots(self):
        result1, result2, result3 = random.choices(SLOTS_ELEMENTS, k=3)
        resulting_elements = [result1, result2, result3]

        jackpot_element = SLOTS_ELEMENTS[0]

        if result1 == result2 == result3:
            if result1 == jackpot_element:
                # Jackpot
                return (SLOTS_BET * SPIN_MULTIPLICATORS['jackpot'], resulting_elements)
            else:
                # Regular
                return (SLOTS_BET * SPIN_MULTIPLICATORS['regular'], resulting_elements)
        elif result1 == result2 or result1 == result3 or result2 == result3:
            # Partial
            return (SLOTS_BET * SPIN_MULTIPLICATORS['partial'], resulting_elements)
        else:
            # Loss
            return (SLOTS_BET * SPIN_MULTIPLICATORS['loss'], resulting_elements)

@login_required
def slots(request):
    if request.method == 'POST':
        slots_game = Slots({},request.user)

        try:
            slots_game.handle_action(request)
        except ValueError as error:
            print(error)
            return JsonResponse({'error': str(error)}, status=400)
        
        return JsonResponse(slots_game.client_state())
    else:
        return HttpResponseBadRequest()
