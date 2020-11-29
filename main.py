from game.custom_environment import CustomEnv
import matplotlib.pyplot as plt
import numpy as np

env = CustomEnv()

LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 3000

epsilone = 0.5
START_EPSILONE_DECAYING = 1
END_EPSILONE_DECAYING = EPISODES // 2
epsilone_decay_value = epsilone/(END_EPSILONE_DECAYING-START_EPSILONE_DECAYING)

DISCRETE_OS_SIZE = [1, 1, 6, 5, 5]

VIEW_FPS = 240

def get_discrete_state(state):
    discrete_state = (state - env.low)/discrete_os_win_size
    return tuple(discrete_state.astype(np.int)) 

try:
    print("Loading q_table")
    q_table = np.load("q_table.npy")
except Exception:
    q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [3]))  #Create array from random number in the range from -2 to 0

discrete_os_win_size = (env.high - env.low )/DISCRETE_OS_SIZE
statistics = []

for episode in range(EPISODES):
    episode_reward = 0
    done = False
    discrete_state = get_discrete_state(env.reset())
    while not done:
        if np.random.random() > epsilone:
            action = np.argmax(q_table[discrete_state])
        else:
            action = np.random.randint(0, 3)
        observation, reward, done = env.step(action)

        episode_reward += reward
        if episode_reward>10:
            env.render(VIEW_FPS)

        new_discrete_state = get_discrete_state(observation)
        
        if not done:
            max_future_q = np.max(q_table[new_discrete_state]) #Maximum number from array 
            current_q = q_table[discrete_state + (action, )] 
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q) 
            q_table[discrete_state+(action,)] = new_q
        elif observation[0] >= 0.5:
            q_table[discrete_state + (action, )] = 0
        discrete_state = new_discrete_state 
    np.save("q_table.npy",q_table) #Save q_table
    statistics.append(episode_reward) 
    if END_EPSILONE_DECAYING >= episode >= START_EPSILONE_DECAYING:
        epsilone -= epsilone_decay_value
    if episode_reward>10:  print(episode, episode_reward)

plt.plot(range(EPISODES), statistics)
plt.show()