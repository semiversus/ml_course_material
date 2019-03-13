from tictactoe import ConnectGame, ConsoleMatrixPlayer, ConnectState
from engine import AlphaBetaPlayer


class ConnectFourGame(ConnectGame):
    def __init__(self):
        ConnectGame.__init__(self, width=7, height=6, n_in_line=4)

    def actions(self, state):
        return [i for i in range(self.width) if state.fields[i] is None]

    def move(self, state, action):
        position = action
        for position in range(action, self.width * self.height, self.width):
            if state.fields[position] is not None:
                break

        position -= self.width
        assert state.fields[position] is None

        fields = state.fields.copy()
        fields[position] = state.player

        if self._is_winning(fields, state.player, position):
            utility = +1 if state.player == 'X' else -1
        else:
            utility = 0

        player = 'X' if state.player == 'O' else 'O'
        return ConnectState(fields=fields, player=player, utility=utility)


if __name__ == '__main__':
    game = ConnectFourGame()
    human = ConsoleMatrixPlayer()
    opponent = AlphaBetaPlayer(depth=8)

    final_state = game.play(human, opponent)

    human.display(game, final_state)

    result = game.utility(final_state, 'X')

    if result == 0:
        print('Game ended in draw')
    elif result > 0:
        print('Player1 (X) wins!')
    else:
        print('Player2 (O) wins!')
