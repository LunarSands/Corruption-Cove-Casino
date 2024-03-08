from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest
import json
import random
from itertools import product

from Corruption_Cove.games.game import Game

SUITS = ['h','s','d','c']
VALUES = ['a','2','3','4','5','6','7','8','9','10','j','q','k']

class Blackjack(Game):
    def __init__(self, state):
        super().__init__(state)
        self.set_state(state)


    def set_state(self, state):
        super().set_state(state)
        self.deck = state.get('deck', construct_deck())
        self.hands = state.get('hands', [])
        self.finished_hands = state.get('finished_hands', [False, True])
        self.dealer_hand = state.get('dealer_hand', [])
        self.double_downs = state.get('double_downs', [False, False])

    def get_state(self):
        return {'deck':self.deck,
                'hands':self.hands,
                'finished_hands': self.finished_hands,
                'dealer_hand':self.dealer_hand,
                'double_downs':self.double_downs,
                **super().get_state()}

    def calculate_winnings(self):
        winnings=0
        if not self.is_finished():
            return 0
        default_bet = self.bets.get('default',0)
        winnings += sum([(default_bet/len(self.hands) + self.bets.get(f'double_down_{i}',0)) * self.hand_return(hand) for i,hand in enumerate(self.hands)])
        return winnings

    def hand_return(self,hand):
        hand_score = self.score_hand(hand)
        dealer_score = self.score_hand(self.dealer_hand)
        if hand_score > 21:
            return 0
        if dealer_score > 21:
            return 2
        if hand_score==21 and len(hand)==2:
            if dealer_score==21 and len(self.dealer_hand)==2:
                return 1
            return 2.5
        if hand_score>dealer_score:
            return 2
        return 0

    def score_hand(self,hand):
        aces = 0
        score = 0
        for card in hand:
            face = card[1]
            if face=='a':
                aces+=1
                score+=11
            else:
                score+= self.card_value(card)
        while score>21 and aces>0:
            score-=10
            aces-=1
        return score

    def is_valid_bet_type(self, bet_type):
        return super().is_valid_bet_type(bet_type)


    def card_value(self,card):
        face = card[1]
        if face.isnumeric():
            return int(face)
        elif face in 'jqk':
            return 10
        else:
            return 11



    def client_state(self):
        return {'hands':self.hands,
                'scores':[self.score_hand(hand) for hand in self.hands],
                'valid_actions':self.get_valid_actions(),
                'dealer_hand':self.dealer_hand,
                'dealer_score':self.score_hand(self.dealer_hand),
                'bets':self.bets,
                'finished':self.is_finished(),
                'winnings':self.calculate_winnings()}

    def is_finished(self):
        return self.finished_hands[0] and self.finished_hands[1]

    def get_valid_actions(self):
        if not self.started or self.is_finished():
            return {'all':['start']}
        if len(self.hands)==0:
            return {'all':['bet']}
        res = {'all':[],'0':[],'1':[]}
        if len(self.hands)==1 and len(self.hands[0])==2 and self.card_value(self.hands[0][0])==self.card_value(self.hands[0][1]):
            res['all'].append('split')
        for i,hand in enumerate(self.hands):
            if self.finished_hands[i]:
                continue
            if self.score_hand(hand)<21:
                res[str(i)].append('hit')
                if not self.double_downs[i]:
                    res[str(i)].append('double_down')
            res[str(i)].append('stay')
        return res

    def handle_start(self, action):
        super().handle_start(action)
        self.hands = [[self.deck.pop(),self.deck.pop()]]
        self.dealer_hand = [self.deck.pop()]
        self.add_bet(action['bet'])

    def dealer_draw(self):
        while self.score_hand(self.dealer_hand)<17:
            self.dealer_hand.append(self.deck.pop())

    def draw_card(self,hand_no):
        self.hands[hand_no].append(self.deck.pop())

    def handle_action_during(self, action_type, action):
        hand_no = action.get('hand_no', 0)
        valid_actions = self.get_valid_actions()
        if action_type not in valid_actions['all'] and action_type not in valid_actions.get(str(hand_no),[]):
            raise ValueError('Invalid action')
        if action_type == 'hit':
            self.draw_card(hand_no)
            score = self.score_hand(self.hands[hand_no])
            if score >= 21:
                self.finished_hands[hand_no] = True
        elif action_type == 'stay':
            self.finished_hands[hand_no] = True
            if self.is_finished():
                self.dealer_draw()
        elif action_type == 'double_down':
            self.add_bet({'type':f'double_down_{hand_no}','amount':self.bets.get('default',0)})
            self.draw_card(hand_no)
        elif action_type == 'split':
            temp = self.hands[0]
            self.hands = [[temp[0]],[temp[1]]]
            self.finished_hands[1] = False
        else:
            super().handle_action_during(action_type,action)

def construct_deck():
    deck = list(product(SUITS,VALUES))
    random.shuffle(deck)
    return deck

def blackjack(request:HttpRequest):
    #TODO: move to the user model instead of session (as JSON field)
    state = request.session.get('blackjack_state',{})
    print(state)
    blackjack_game = Blackjack(state)
    if request.method=='GET':
        return JsonResponse(blackjack_game.client_state())
    elif request.method=='POST':
        action = json.loads(request.body)
        try:
            print(action)
            blackjack_game.handle_action(action)
        except ValueError as e:
            print(e)
            return HttpResponseBadRequest()
        request.session['blackjack_state'] = blackjack_game.get_state()
        print(request.session['blackjack_state'])
        return JsonResponse(blackjack_game.client_state())
    return HttpResponseBadRequest()