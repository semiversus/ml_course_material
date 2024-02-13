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
        return self.parent.solution() + [self.action]
    
    
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


goal_state = breadth_first_search(Hanoi(((1, 2, 3, 4, 5), (), ())))
print(goal_state.solution())