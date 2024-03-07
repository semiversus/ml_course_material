from typing import TypeVar, Generic


StateT = TypeVar('StateT')
ActionT = TypeVar('ActionT')


class Node(Generic[StateT, ActionT]):
    def __init__(self, state: StateT, parent: 'Node' = None, action: ActionT = None):
        self.state = state
        self.parent = parent
        self.action = action

    def solution(self) -> list[ActionT]:
        if self.parent is None:
            return []
        return self.parent.solution() + [self.action, self.state]


class SearchProblem(Generic[StateT, ActionT]):
    def __init__(self, initial_state: StateT):
        self.initial_state = initial_state

    def actions(self, state: StateT) -> set[ActionT]:
        raise NotImplementedError

    def result(self, node: Node, action: ActionT) -> Node[StateT, ActionT]:
        raise NotImplementedError

    def is_goal_state(self, state: StateT) -> bool:
        raise NotImplementedError


def breadth_first_search(problem: SearchProblem[StateT, ActionT]) -> Node[StateT, ActionT]:
    frontier = [Node(problem.initial_state)]
    explored = set()

    while frontier:
        node = frontier.pop(0)
        if problem.is_goal_state(node.state):
            return node
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = problem.result(node, action)
            if child.state not in explored and child not in frontier:
                frontier.append(child)
    return None


class Hanoi(SearchProblem):
    def actions(self, state):
        action_list = list()
        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                if (state[i] and not state[j]) or (state[i] and state[i][0] < state[j][0]):
                    action_list.append((i, j))

        return action_list

    def result(self, node, action):
        i, j = action
        new_state = tuple(map(list, node.state))
        new_state[j].insert(0, new_state[i].pop(0))
        new_state = tuple(map(tuple, new_state))
        return Node(new_state, node, action)

    def is_goal_state(self, state):
        return not state[0] and not state[1] and tuple(sorted(state[2])) == state[2]


class NPuzzle(SearchProblem):
    def actions(self, state):
        empty_index = state.index(None)
        actions = set()
        if empty_index > 3:
            actions.add('up')
        if empty_index < 12:
            actions.add('down')
        if empty_index % 4 != 0:
            actions.add('left')
        if empty_index % 4 != 3:
            actions.add('right')
        return actions

    def result(self, node, action):
        empty_index = node.state.index(None)
        state = list(node.state)
        if action == 'down':
            new_state = state[:empty_index] + [state[empty_index + 4]] + state[empty_index + 1:empty_index + 4] + [None]
            if empty_index < 11:
                new_state += state[empty_index + 5:]
        elif action == 'up':
            new_state = state[:empty_index - 4] + [None] + state[empty_index - 3:empty_index] + [state[empty_index - 4]] + state[empty_index + 1:]
        elif action == 'left':
            new_state = state[:empty_index - 1] + [None] + [state[empty_index - 1]] + state[empty_index + 1:]
        else:
            new_state = state[:empty_index] + [state[empty_index + 1]] + [None] + state[empty_index + 2:]

        return Node(tuple(new_state), node, action)

    def is_goal_state(self, state) -> bool:
        return state == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, None)


goal_state = breadth_first_search(Hanoi(((1, 2, 3, 4, 5), (), ())))
print(goal_state.solution())

import random
l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, None]

for i in range(10):
    action = random.choice(list(NPuzzle(l).actions(l)))
    print(l, action)
    l = list(NPuzzle(l).result(Node(tuple(l)), action).state)

goal_state = breadth_first_search(NPuzzle(tuple(l)))
print(goal_state.solution())
