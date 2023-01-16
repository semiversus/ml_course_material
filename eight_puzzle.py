import random
from collections import deque
import heapq


class Node:
    def is_goal(self) -> bool:
        return False

    def dump(self):
        pass

    def extend(self):
        pass


def breadth_first_search(start_node: Node):
    open_nodes = deque([start_node])
    visited_nodes = set()

    while open_nodes:
        node = open_nodes.popleft()

        if node in visited_nodes:
            continue

        visited_nodes.add(node)

        if node.is_goal():
            node.dump()
            break

        open_nodes += node.extend()


def depth_first_search(start_node: Node):
    open_nodes = [start_node]
    visited_nodes = set()

    while open_nodes:
        node = open_nodes.pop()

        if node in visited_nodes:
            continue

        visited_nodes.add(node)

        if node.is_goal():
            node.dump()
            break

        open_nodes += node.extend()


def a_star_search(start_node: Node):
    open_nodes = [(float('inf'), start_node)]
    visited_nodes = set()

    iterations = 0
    while open_nodes:
        _, node = heapq.heappop(open_nodes)
        visited_nodes.add(node)

        if node.is_goal():
            node.dump()
            print(iterations)
            break

        for n in node.extend():
            if n not in visited_nodes:
                heapq.heappush(open_nodes, (n.cost + n.heuristic, n))

class EightPuzzle(Node):
    WIDTH = 3
    HEIGHT = 3

    def __init__(self, state: list, parent=None, history=()):
        self.state = state
        self.parent = parent
        self.history = history

    @property
    def cost(self):
        return len(self.history)

    @property
    def heuristic(self):
        return sum(m != n for m, n in zip(self.state, list(range(1, self.WIDTH * self.HEIGHT)) + [None]))

    def is_goal(self) -> bool:
        return self.state[:-1] == list(range(1, self.WIDTH * self.HEIGHT))

    def dump(self):
        print('Movements: ', ' '.join(self.history))
        for index, number in enumerate(self.state):
            if number is not None:
                print(f'{number:3}', end='')
            else:
                print('   ', end='')

            if (index + 1) % self.WIDTH == 0:
                print()

        assert len(self.state) == 9

    @classmethod
    def get_random_state(self, iterations=100):
        node = EightPuzzle(list(range(1, self.WIDTH * self.HEIGHT)) + [None])

        for _ in range(iterations):
            node = random.choice(node.extend())

        return EightPuzzle(node.state)

    def extend(self):
        nodes = []
        empty_index = self.state.index(None)
        x, y = empty_index % self.WIDTH, empty_index // self.WIDTH

        if x != 0:
            state = self.state[:empty_index - 1] + [None, self.state[empty_index - 1]] + self.state[empty_index + 1:]
            nodes.append(EightPuzzle(state, parent=self, history=self.history + ('Left',)))

        if x != self.WIDTH - 1:
            state = self.state[:empty_index] + [self.state[empty_index + 1], None] + self.state[empty_index + 2:]
            nodes.append(EightPuzzle(state, parent=self, history=self.history + ('Right',)))

        if y != 0:
            state = self.state[:empty_index - self.WIDTH] + [None] + self.state[empty_index - self.WIDTH + 1:empty_index] + [self.state[empty_index - self.WIDTH]] + self.state[empty_index + 1:]
            nodes.append(EightPuzzle(state, parent=self, history=self.history + ('Up',)))

        if y != self.HEIGHT - 1:
            state = self.state[:empty_index] + [self.state[empty_index + self.WIDTH]] + self.state[empty_index + 1: empty_index + self.WIDTH] + [None] + self.state[empty_index + self.WIDTH + 1:]
            nodes.append(EightPuzzle(state, parent=self, history=self.history + ('Down',)))

        return nodes

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        return hash(tuple(self.state))


start_node = EightPuzzle.get_random_state(100)
start_node.dump()
breadth_first_search(start_node)
#depth_first_search(start_node)
a_star_search(start_node)
