"""
Flappy Bird Q-Learning Workshop Template
Author: [Your Name]
Instructions: Fill in the TODOs and experiment with Q-learning to train the AI!
"""

import numpy as np
import random

ai_on = False  # TODO: set True to enable AI

# =========================
# Q-TABLE INITIALIZATION
# =========================
# TODO: Initialize a 3D Q-table with shape (7, 21, 2) filled with zeros
# 7 = discretized horizontal distance to pipe
# 21 = discretized vertical distance to pipe
# 2 = # of action options (jump or don't jump)
Q = np.zeros((__, __, __)) 

# =========================
# STATE DISCRETIZATION FUNCTION
# =========================
def pipe_relative_to_bird(birdxpos, birdypos, bttm_pipes):
    """
    Maps continuous bird position to discrete state for Q-learning.
    """
    # TODO: compute horizontal distance to the closest bottom pipe
    x = min(280, bttm_pipes[0]['x'] - ____)
    
    # Note: Pygame Y coordinate increases downwards!

    y = ____ # TODO: set vertical distance from bottom pipe to bird
    if y < 0:
        SCREEN_HEIGHT = 511
        BASE_Y = SCREEN_HEIGHT * 0.8
        y = abs(y) + BASE_Y

    # discretize state space
    return int(x / __ - 1), int(y / __)  # TODO: adjust for discretization

# =========================
# Q-LEARNING UPDATE
# =========================
def Q_update(x_prev, y_prev, jump, reward_or_penalty, x_new, y_new):
    """
    Updates Q-table using the Bellman equation.
    Q(s, a) ← (1 - α) * Q(s, a) + α * [ r + γ * max(Q(s', a')) - Q(s, a) ]

    where:
        s   = current state
        a   = action taken in state s
        r   = reward/penalty received after taking action a
        s'  = next state after action a
        a'  = possible actions in state s'
        α   = learning rate (0 < α ≤ 1)
        γ   = discount factor (0 ≤ γ ≤ 1)

    """


    # TODO: fill in the Bellman equation
    if jump:
        Q[x_prev][y_prev][1] = 0.4 * _____ + \
                               (0.6) * (reward_or_penalty + max(_____, _____))
    else:
        Q[x_prev][y_prev][0] = 0.4 * _____ + \
                               (0.6) * (reward_or_penalty + max(_____, _____))


# =========================
# REWARD FUNCTIONS
# =========================
def ai_crashed(x_prev, y_prev, jump, x_new, y_new):
    penalty = ___  # TODO: set reward for not crashing
    Q_update(x_prev, y_prev, jump, penalty, x_new, y_new)

def ai_didnt_crash(x_prev, y_prev, jump, x_new, y_new):
    reward = ___  # TODO: set reward for not crashing
    Q_update(x_prev, y_prev, jump, reward, x_new, y_new)

def ai_passed_pipe(x_prev, y_prev, jump, x_new, y_new):
    reward = ___  # TODO: set reward for passing a pipe
    Q_update(x_prev, y_prev, jump, reward, x_new, y_new)


# =========================
# AI DECISION FUNCTION
# =========================
def ai_play(x, y):
    """
    Returns True to jump, False to do nothing.
    """
    # TODO: set the jump variables

    jump = ___  

    if Q[x][y][1] > Q[x][y][0]:
        jump = ___
    
    return jump







# =========================
# OPTIONAL: EPSILON-GREEDY STRATEGY
# =========================
# TODO: Uncomment and fix the code below to implement epsilon-greedy exploration
#       MAKE SURE TO COMMENT LINE 86 AND UNCOMMENT LINE 87 AND 163 IN FlappyBird.py
# epsilon = 0.2
# epsilon_min = 0.00001
# epsilon_decay = 0.8
# def epsilon_greedy_ai_play(x, y):
#     global epsilon
#     jump = ___
#     if random.uniform(0, 1) < epsilon:
#         jump = random.choice([False, False, False, True])
#     else:
#         if Q[x][y][1] > Q[x][y][0]:
#             jump = True
#     return jump
# 
# def decay_epsilon():
#     global epsilon
#     if epsilon > epsilon_min:
#         epsilon *= ___

