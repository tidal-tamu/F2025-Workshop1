import numpy
import random

# Manual play or AI play
ai_on = False

# Initialize Q-table
Q = numpy.zeros((7,21,2), dtype=float)

def pipe_relative_to_bird(birdxpos, birdypos, bttm_pipes):
    x = min(280, bttm_pipes[0]['x'] - birdxpos)
    y = bttm_pipes[0]['y'] - birdypos
    if y < 0:
        SCREEN_HEIGHT = 511
        BASE_Y = SCREEN_HEIGHT * 0.8
        y = abs(y) + BASE_Y
    return int(x / 40 - 1), int(y / 40)

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
    reward = 30
    Q_update(x_prev, y_prev, jump, reward, x_new, y_new)

def ai_play(x, y):
    jump = False
    
    if Q[x][y][1] > Q[x][y][0]:
        jump = True

    return jump





# epsilon = 0.2
# epsilon_min = 0.00001
# epsilon_decay = 0.8
# def epsilon_greedy_ai_play(x, y):
#     global epsilon
#     jump = False
#     if random.uniform(0, 1) < epsilon:
#         jump = random.choice([False, False, False, True])
#     else:
#         if Q[x][y][1] > Q[x][y][0]:
#             jump = True
#     return jump

# def decay_epsilon():
#     global epsilon
#     if epsilon > epsilon_min:
#         epsilon *= epsilon_decay
