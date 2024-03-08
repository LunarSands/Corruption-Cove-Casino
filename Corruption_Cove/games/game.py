class Game:
    def __init__(self, state):
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
        bet_type = bet.get('bet_type', 'default')
        amount = bet.get('amount', 0)
        if self.is_valid_bet_type(bet_type):
            if amount <= 0:
                raise ValueError('Invalid bet amount')
            # TODO: verify funds and remove from account
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
            self.clear()
        elif action_type == 'start':
            self.handle_start(action)
        elif self.started:
            self.handle_action_during(action_type, action)
        else:
            raise ValueError('Unknown action')
