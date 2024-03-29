from json import JSONDecodeError

from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest
import json
import random
from itertools import product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from Corruption_Cove.games.game import Game
from Corruption_Cove.models import UserProfile, Dealer

SUITS = ['h', 's', 'd', 'c']
VALUES = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k']
BLACKJACK_BET_TYPES = ['double_down_0','double_down_1']

class Blackjack(Game):
    def __init__(self, state, user,dealer):
        super().__init__(state,user)
        self.set_state(state)
        self.name = 'blackjack-'+dealer.name
        self.dealer = dealer

    def set_state(self, state):
        super().set_state(state)
        self.deck = state.get('deck', construct_deck())
        self.hands = state.get('hands', [])
        self.finished_hands = state.get('finished_hands', [False, True])
        self.dealer_hand = state.get('dealer_hand', [])
        self.double_downs = state.get('double_downs', [False, False])
        self.winnings = state.get('winnings',0)

    def get_state(self):
        return {'deck': self.deck,
                'hands': self.hands,
                'finished_hands': self.finished_hands,
                'dealer_hand': self.dealer_hand,
                'double_downs': self.double_downs,
                'winnings': self.winnings,
                **super().get_state()}

    def calculate_winnings(self):
        winnings = 0
        if not self.is_finished():
            return 0
        default_bet = self.bets.get('default', 0)
        winnings += sum(
            [(default_bet / len(self.hands) + self.bets.get(f'double_down_{i}', 0)) * self.hand_return(hand) for i, hand
             in enumerate(self.hands)])
        return winnings

    def hand_return(self, hand):
        hand_score = self.score_hand(hand)
        dealer_score = self.score_hand(self.dealer_hand)
        if hand_score > 21:
            return 0
        if dealer_score > 21:
            return 2
        if hand_score == 21 and len(hand) == 2:
            if dealer_score == 21 and len(self.dealer_hand) == 2:
                return 1
            return 2.5
        if hand_score > dealer_score:
            return 2
        return 0

    def score_hand(self, hand):
        aces = 0
        score = 0
        for card in hand:
            face = card[1]
            if face == 'a':
                aces += 1
                score += 11
            else:
                score += self.card_value(card)
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score

    def is_valid_bet_type(self, bet_type):
        if len(self.bets)==0:
            return bet_type=='default'
        return super().is_valid_bet_type(bet_type) or bet_type in BLACKJACK_BET_TYPES

    def card_value(self, card):
        face = card[1]
        if face.isnumeric():
            return int(face)
        elif face in 'jqk':
            return 10
        else:
            return 11

    def client_state(self):
        return {'hands': self.hands,
                'scores': [self.score_hand(hand) for hand in self.hands],
                'valid_actions': self.get_valid_actions(),
                'dealer_hand': self.dealer_hand,
                'dealer_score': self.score_hand(self.dealer_hand),
                'bets': self.bets,
                'finished': self.is_finished(),
                'winnings': self.winnings}

    def is_finished(self):
        return self.finished_hands[0] and self.finished_hands[1]

    def get_valid_actions(self):
        if not self.started or self.is_finished():
            return {'all': ['start']}
        if len(self.hands) == 0:
            return {'all': ['bet']}
        res = {'all': [], '0': [], '1': []}
        if len(self.hands) == 1 and len(self.hands[0]) == 2 and self.card_value(self.hands[0][0]) == self.card_value(
                self.hands[0][1]):
            res['all'].append('split')
        for i, hand in enumerate(self.hands):
            if self.finished_hands[i]:
                continue
            if self.score_hand(hand) < 21:
                res[str(i)].append('hit')
                if not self.double_downs[i]:
                    res[str(i)].append('double_down')
            res[str(i)].append('stay')
        return res

    def handle_start(self, action):
        super().handle_start(action)
        self.hands = [[self.deck.pop(), self.deck.pop()]]
        self.dealer_hand = [self.deck.pop()]
        self.place_bet(action.get('bet'))

    def dealer_draw(self):
        while self.score_hand(self.dealer_hand) < self.dealer.stop:
            self.dealer_hand.append(self.deck.pop())
        self.winnings = self.calculate_winnings()
        self.add_bet_results(self.winnings)


    def draw_card(self, hand_no):
        self.hands[hand_no].append(self.deck.pop())

    def handle_action_during(self, action_type, action):
        hand_no = action.get('hand_no', 0)
        valid_actions = self.get_valid_actions()
        if action_type not in valid_actions['all'] and action_type not in valid_actions.get(str(hand_no), []):
            raise ValueError('Invalid action')
        if action_type == 'hit':
            self.draw_card(hand_no)
            score = self.score_hand(self.hands[hand_no])
            if score >= 21:
                self.finished_hands[hand_no] = True
        elif action_type == 'stay':
            self.finished_hands[hand_no] = True
        elif action_type == 'double_down':
            self.place_bet({'type': f'double_down_{hand_no}', 'amount': self.bets.get('default', 0)})
            self.draw_card(hand_no)
            self.finished_hands[hand_no]=True
        elif action_type == 'split':
            temp = self.hands[0]
            self.hands = [[temp[0]], [temp[1]]]
            self.finished_hands[1] = False
        else:
            super().handle_action_during(action_type, action)
        if self.is_finished():
            self.dealer_draw()


def construct_deck():
    deck = list(product(SUITS, VALUES))
    random.shuffle(deck)
    return deck


@login_required
def blackjack(request: HttpRequest, dealer=""):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    state = profile.blackjack_state
    try:
        dealer_model = Dealer.objects.get(name=dealer)
    except:
        return HttpResponseBadRequest()
    try:
        state = json.loads(state)
    except JSONDecodeError:
        state = {}
    print(state)
    blackjack_game = Blackjack(state, user, dealer_model)
    if request.method == 'GET':
        return JsonResponse(blackjack_game.client_state())
    elif request.method == 'POST':
        try:
            blackjack_game.handle_action(request)
        except ValueError as e:
            print(e)
            return HttpResponseBadRequest()
        profile.blackjack_state = json.dumps(blackjack_game.get_state())
        print(profile.blackjack_state)
        profile.save()
        return JsonResponse(blackjack_game.client_state())
    return HttpResponseBadRequest()
