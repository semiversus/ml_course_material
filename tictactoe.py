from engine import Game, Player, MinMaxPlayer, RandomPlayer
from collections import namedtuple

ConnectState = namedtuple('State', 'fields player utility')


class ConnectGame(Game):
    def __init__(self, width=3, height=3, n_in_line=3):
        self.width = width
        self.height = height
        self.n_in_line = n_in_line

    @property
    def init_state(self):
        fields = [None] * self.width * self.height
        return ConnectState(fields=fields, player='X', utility=0)

    def actions(self, state):
        return [i for (i, s) in enumerate(state.fields) if s is None]

    def move(self, state, action):
        assert state.fields[action] is None

        fields = state.fields.copy()
        fields[action] = state.player

        if self._is_winning(fields, state.player, action):
            utility = +1 if state.player == 'X' else -1
        else:
            utility = 0

        player = 'X' if state.player == 'O' else 'O'
        return ConnectState(fields=fields, player=player, utility=utility)

    def terminal(self, state):
        no_field_left = all(i is not None for i in state.fields)
        return (state.utility != 0) or no_field_left

    def _is_winning(self, fields, player, action):
        def check_delta(fields, player, action, delta):
            n = 0

            column_prev, row_prev = None, None
            for pos in range(action, len(fields), delta):
                if fields[pos] != player:
                    break

                # check for column or row overflow
                column, row = pos % self.width, pos // self.width
                if column_prev is not None:
                    if abs(column_prev - column) > 1:
                        break
                    if abs(row_prev - row) > 1:
                        break
                column_prev, row_prev = column, row

                n += 1

            column_prev, row_prev = None, None
            for pos in range(action, -1, -delta):
                if fields[pos] != player:
                    break

                # check for column or row overflow
                column, row = pos % self.width, pos // self.width
                if column_prev is not None:
                    if abs(column_prev - column) > 1:
                        break
                    if abs(row_prev - row) > 1:
                        break
                column_prev, row_prev = column, row

                n += 1

            return n > self.n_in_line

        for delta in (1, self.width, self.width - 1, self.width + 1):
            if check_delta(fields, player, action, delta):
                return True

        return False

    def utility(self, state, player):
        return state.utility if player == 'X' else -state.utility

    def player(self, state):
        return state.player


class ConsoleMatrixPlayer(Player):
    def query(self, game, state):
        self.display(game, state)

        while True:
            try:
                field_number = int(input('Enter your move:'))
            except TypeError:
                continue

            if field_number in game.actions(state):
                return field_number

            print('Move is not allowed')

    def display(self, game, state):
        for y in range(game.height):
            for x in range(game.width):
                field_char = state.fields[x + y*game.width]
                print(' ' if field_char is None else field_char, end='')
            print()


if __name__ == '__main__':
    game = ConnectGame()
    human = ConsoleMatrixPlayer()
    opponent = MinMaxPlayer()

    final_state = game.play(human, opponent)

    human.display(game, final_state)

    result = game.utility(final_state, 'X')

    if result == 0:
        print('Game ended in draw')
    elif result > 0:
        print('Player1 (X) wins!')
    else:
        print('Player2 (O) wins!')
