""" Use bipedal walker and evolutionary algoritum to maximize various parameters
In this example the walker tries to maximize it's own rotation

See https://gymnasium.farama.org/environments/box2d/bipedal_walker/
"""
from random import randint, uniform

import gymnasium as gym

BEST_N = 10
COPIES = 20
SIMULATION_STEPS = 300

def fitness(actions, render=False) -> float:
    env = gym.make("BipedalWalker-v3", render_mode='human' if render else None)
    env.reset(seed=0)

    f = 0

    for action in actions:
        obs = env.step(action)
        f += -obs[0][1]  # use angle

    return f

def iterate(instances):
    # copy
    instances = [list(l) for l in instances * COPIES]

    # modify
    for instance in instances[BEST_N:]:
        for _ in range(randint(1, 20)):
            start = randint(0, len(instance) - 1)
            duration = min(len(instance) - 1, int(10 ** uniform(0, 3)))
            joint_index = randint(0, 3)
            speed = uniform(-1, 1)
            if uniform(0, 1) < 0.05:
                instance[start:start+duration] = []
                instance += [(0, 0, 0, 0)] * duration
            else:
                for index in range(start, duration):
                    instance[index] = tuple(instance[index][:joint_index] + (speed,) + instance[index][joint_index + 1:])

    # check fitness
    best_instances = []
    for instance in instances:
        best_instances.append( (fitness(instance), instance) )

    return list(i[1] for i in sorted(best_instances, key=lambda i: i[0], reverse=True)[:BEST_N])

instances = [[(0, 0, 0, 0)] * SIMULATION_STEPS] * BEST_N

generation = 1
while True:
    print(f'Generation {generation}')
    instances = iterate(instances)

    print(f'y_max={fitness(instances[0], render=True):.2f}')

    generation += 1
