from Corruption_Cove.models import Bet,Bank
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

    def add_bet(self, bet):
        bet_type = bet.get('type', 'default')
        amount = bet.get('amount', 0)
        if self.is_valid_bet_type(bet_type):
            if amount < 0:
                raise ValueError('Invalid bet amount')
            # TODO: verify funds and remove from account
            cards = Bank.objects.filter(username=user)
            card = next((card for card in cards if card.balance>=amount),None)
            if card is None:
                pass
                # uncomment to require funds in order to bet
                # raise ValueError('No card exists with enough funds')
            else:
                card.balance -= amount
                card.save()                
            Bet.objects.create(username=user,game=self.name,amount=amount).save()
            self.bets[bet_type] = self.bets.get(bet_type, 0) + amount

    def handle_action_during(self, action_type, action):
        if action_type == "bet":
            bet = action.get('bet')
            if bet is None:
                raise ValueError('Invalid bet')
            self.add_bet(bet)
        else:
            raise ValueError('Unknown action')

    def handle_action(self, action):
        action_type = action.get('action')
        if action_type is None:
            raise ValueError('No action type')
        if action_type == 'clear':
            #TODO: this should be admin only or removed
            self.clear()
        elif action_type == 'start':
            self.handle_start(action)
        elif self.started:
            self.handle_action_during(action_type, action)
        else:
            raise ValueError('Unknown action')
