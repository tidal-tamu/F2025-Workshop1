import numpy
import random

# Manual play or AI play
ai_on = True

# Initialize Q-table
Q = numpy.zeros((7,21,2), dtype=float)

def bird_relative_to_pipe(birdxpos, birdypos, bttm_pipes):
    x = min(280, bttm_pipes[0]['x'])
    y = bttm_pipes[0]['y'] - birdypos
    if y < 0:
        y = abs(y) + 408
    return int(x/40 - 1), int(y/40)

def Q_update(x_prev, y_prev, jump, reward, x_new, y_new):
    if jump:
        Q[x_prev][y_prev][1] = 0.4 * Q[x_prev][y_prev][1] + \
                               (0.6) * (reward + max(Q[x_new][y_new][0], Q[x_new][y_new][1]))
    else:
        Q[x_prev][y_prev][0] = 0.4 * Q[x_prev][y_prev][0] + \
                               (0.6) * (reward + max(Q[x_new][y_new][0], Q[x_new][y_new][1]))

def ai_crashed(x_prev, y_prev, jump, x_new, y_new):
    reward = -1000
    Q_update(x_prev, y_prev, jump, reward, x_new, y_new)

def ai_didnt_crash(x_prev, y_prev, jump, x_new, y_new):
    reward = 15
    Q_update(x_prev, y_prev, jump, reward, x_new, y_new)

def ai_passed_pipe(x_prev, y_prev, jump, x_new, y_new):
    reward = 15
    Q_update(x_prev, y_prev, jump, reward, x_new, y_new)

def ai_play(x, y):
    jump = False
    
    if Q[x][y][1] > Q[x][y][0]:
        jump = True

    return jump



'''

If you would like to experiment with early random actions, uncomment the code below.

Epsilon-greedy action selection is a common strategy in reinforcement learning to balance exploration and exploitation.
It is done by doing a random action by choosing a random number between 0 and 1 and if it is less than epsilon, 
the AI will do a random action.

'''


# # Epsilon-greedy params
# epsilon = 1.0
# epsilon_min = 0.01
# epsilon_decay = 0.5  # shrink a little each episode
# def epsilon_greedy_ai_play(x, y):
#     global epsilon
#     jump = False
    
#     # epsilon-greedy: explore sometimes
#     if random.uniform(0, 1) < epsilon:
#         jump = random.choice([False, True])
#         print(epsilon)
#     else:
#         if Q[x][y][1] > Q[x][y][0]:
#             jump = True

#     return jump

# def decay_epsilon():
#     global epsilon
#     if epsilon > epsilon_min:
#         epsilon *= epsilon_decay
