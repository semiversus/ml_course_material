from time import sleep
from random import randint, uniform

import gymnasium as gym
env_calculate = gym.make("BipedalWalker-v3", render_mode=None)
env_render = gym.make("BipedalWalker-v3", render_mode='human')

BEST_N = 5
COPIES = 10

def fitness(actions, render=False) -> float:
    f, max_f, sum_f = 0, 0, 0
    env = env_render if render else env_calculate
    env.reset(seed=0)

    for action in actions:
        obs = env.step(action)
        f += obs[0][3]
        max_f = max(f, max_f)

    return max_f

def iterate(instances):
    # copy
    instances = [list(l) for l in instances * COPIES]

    # modify
    for instance in instances:
        for _ in range(randint(1, 20)):
            start = randint(0, len(instance) - 1)
            duration = min(len(instance) - 1, int(10 ** uniform(0, 3)))
            joint_index = randint(0, 3)
            speed = uniform(-1, 1)
            for index in range(start, duration):
                instance[index] = tuple(instance[index][:joint_index] + (speed,) + instance[index][joint_index + 1:])

    # check fitness
    best_instances = []
    for instance in instances:
        best_instances.append( (fitness(instance), instance) )

    return list(i[1] for i in sorted(best_instances, key=lambda i: i[0], reverse=True)[:BEST_N])

instances = [[(0, 0, 0, 0)] * 500] * BEST_N

generation = 1
while True:
    print(f'Generation {generation}')
    instances = iterate(instances)

    if generation % 10 == 0:
        print(f'y_max={fitness(instances[0], render=True):.2f}')

    generation += 1
