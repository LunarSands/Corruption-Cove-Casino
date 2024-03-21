import json
import random
from json import JSONDecodeError
from Corruption_Cove.models import Bet,Bank,UserProfile

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest

from Corruption_Cove.games.game import Game

red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black = [x for x in range(1,37) if x not in red]
positions = ['1st','2nd','3rd']
# noinspection PyTypeChecker
ROULETTE_BETS = [{"type":f"bet-{x}","name":str(x),"req":[x],"return":36} for x in range(37)]+\
                [{"type":f"bet-row{x+1}","name":"2:1","req":range(3-x,37,3),"return":3} for x in range(3)]+\
                [{"type":f"bet-{positions[x]}","name":positions[x]+ " 12","req":range(1+12*x,13+12*x),"return":3} for x in range(3)]+\
                [{"type":"bet-low","name":"1-18","req":range(1,19),"return":2},
                 {"type":"bet-high","name":"19-36","req":range(19,37),"return":2},
                 {"type":"bet-even","name":"Even","req":range(0,37,2),"return":2},
                 {"type":"bet-odd","name":"Odd","req":range(1,37,2),"return":2},
                 {"type":"bet-red","name":"Red","req":red,"return":2},
                 {"type":"bet-black","name":"Black","req":black,"return":2}]

ROULETTE_BET_TYPES = [x['type'] for x in ROULETTE_BETS]



class Roulette(Game):
    def __init__(self,state,user):
        super().__init__(state,user)
        self.result = None
        self.winnings = 0
        self.name="roulette"

    def handle_start(self, action):
        client_bets = action.get('bets')
        if type(client_bets) is not list:
            raise ValueError('Invalid bets')
        for bet in client_bets:
            self.place_bet(bet)
        self.winnings = self.calculate_winnings()
        self.add_bet_results(self.winnings)

    def client_state(self):
        return {'result':self.result,'winnings':self.winnings}

    def is_valid_bet_type(self, bet_type):
        return bet_type in ROULETTE_BET_TYPES

    def calculate_winnings(self):
        if self.result is None:
            self.result = random.randint(0,36)
        winnings = 0
        for bet_data in ROULETTE_BETS:
            if self.result in bet_data['req']:
                winnings += self.bets.get(bet_data['type'],0) * bet_data['return']
        return winnings

@login_required
def play_roulette(request):
    if request.method == "GET":
        return HttpResponseBadRequest()
    elif request.method == "POST":
        roulette_game = Roulette({},request.user)
        try:
            print(request.body)
            roulette_game.handle_action(request)
        except ValueError as e:
            print(e)
            return HttpResponseBadRequest()
        print(roulette_game.client_state())
        return JsonResponse(roulette_game.client_state())
