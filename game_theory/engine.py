class Game:
    @property
    def init_state(self):
        return None

    def actions(self, state):
        return []

    def move(self, state, action):
        return None

    def terminal(self, state):
        return False

    def utility(self, state, player):
        return 0

    def player(self, state):
        return None

    def play(self, player1, player2):
        state = self.init_state
        current_player = player1

        while not self.terminal(state):
            action = current_player.query(self, state)
            state = self.move(state, action)
            current_player = player2 if current_player is player1 else player1

        return state


class Player:
    def query(self, game, state):
        return None


class RandomPlayer(Player):
    def query(self, game, state):
        from random import choice
        return choice(game.actions(state))


class MinMaxPlayer(Player):
    def query(self, game, state):
        player = game.player(state)

        def max_value(state):
            if game.terminal(state):
                return game.utility(state, player)
            v = -float('inf')
            for action in game.actions(state):
                v = max(v, min_value(game.move(state, action)))
            return v

        def min_value(state):
            if game.terminal(state):
                return game.utility(state, player)
            v = float('inf')
            for action in game.actions(state):
                v = min(v, max_value(game.move(state, action)))
            return v

        return max(game.actions(state),
                   key=lambda a: min_value(game.move(state, a)))


class AlphaBetaPlayer(Player):
    def __init__(self, depth=5):
        self.depth = depth

    def query(self, game, state):
        player = game.player(state)

        def max_value(state, alpha, beta, depth):
            if game.terminal(state) or depth > self.depth:
                return game.utility(state, player)

            v = -float('inf')
            for a in game.actions(state):
                v = max(v, min_value(game.move(state, a),
                                     alpha, beta, depth + 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth):
            if game.terminal(state) or depth > self.depth:
                return game.utility(state, player)

            v = float('inf')
            for a in game.actions(state):
                v = min(v, max_value(game.move(state, a),
                                     alpha, beta, depth + 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        best_score = -float('inf')
        beta = float('inf')
        best_action = None
        for a in game.actions(state):
            v = min_value(game.move(state, a), best_score, beta, 1)
            if v > best_score:
                best_score = v
                best_action = a
        return best_action
