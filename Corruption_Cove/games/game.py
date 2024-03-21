import json
from Corruption_Cove.models import Bet,Bank,UserProfile
class Game:
    def __init__(self, state,user):
        self.user = user
        self.name=""
        self.set_state(state)

    def set_state(self, state):
        self.started = state.get('started', False)
        self.bets = state.get('bets', {})

    def get_state(self):
        return {'started': self.started, 'bets': self.bets}

    def handle_start(self, action):
        if self.started and not self.is_finished():
            raise ValueError('Invalid action')
        self.clear()
        self.started = True

    def is_finished(self):
        pass

    def is_valid_bet_type(self, bet_type):
        return bet_type == 'default'

    def clear(self):
        self.set_state({})

    def place_bet(self,bet):
        bet_type = bet.get('type', 'default')
        amount = bet.get('amount', 0)
        if not self.is_valid_bet_type(bet_type):
            raise ValueError('Invalid bet type')
        self.bets[bet_type] = self.bets.get(bet_type, 0) + amount
        user_prof = UserProfile.objects.get(user=self.user)
        card = Bank.objects.get(username=user_prof)
        if card is None:
            raise ValueError('No card exists')
        else:
            card.balance -= amount
            card.save()


    def add_bet_results(self, winnings):
        user_prof = UserProfile.objects.get(user=self.user)
        card = Bank.objects.get(username=user_prof)
        if card is None:
            raise ValueError('No card exists')
        else:
            card.balance += winnings
            card.save()
        losses = sum(bet for bet in self.bets.values())
        new_bet = Bet.objects.create(username=user_prof,game=self.name,amount=winnings-losses)
        new_bet.save()

    def handle_action_during(self, action_type,action):
        if action_type == "bet":
            bet = action.get('bet')
            if bet is None:
                raise ValueError('Invalid bet')
            self.place_bet(bet)
        else:
            raise ValueError('Unknown action')

    def handle_action(self, request):
        action = json.loads(request.body)
        action_type = action.get('action')
        if action_type is None:
            raise ValueError('No action type')
        # if action_type == 'clear':
        #     self.clear()
        elif action_type == 'start':
            self.handle_start(action)
        elif self.started:
            self.handle_action_during(action_type,action)
        else:
            raise ValueError('Unknown action')
