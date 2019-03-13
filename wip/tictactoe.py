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
        pass

    def actions(self, state):
        pass

    def move(self, state, action):
        pass

    def terminal(self, state):
        pass

    def _is_winning(self, fields, player, position):
        def check_delta(fields, player, position, delta):
            n = 0

            column_prev, row_prev = None, None
            for pos in range(position, len(fields), delta):
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
            for pos in range(position, -1, -delta):
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
            if check_delta(fields, player, position, delta):
                return True

        return False

    def utility(self, state, player):
        pass

    def player(self, state):
        pass


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
    pass
