import numpy as np
import gymnasium as gym
from gymnasium.utils.play import play, PlayPlot

from datetime import datetime, date

num_episodes = 1000
env = gym.make("LunarLander-v2", render_mode="rgb_array")

ep_rew = []
rewards = []


def callback(obs_t, obs_tp1, action, rew, terminated, truncated, info):
    global rewards, ep_rew
    ep_rew.append(rew)
    if terminated:
        rewards.append(ep_rew)
        ep_rew = []
    return [rew,]


def play_game(num_episodes):
    play(num_episodes, env, keys_to_action={
        "w": 2,
        "a": 1,
        "d": 3
    }, noop=0, callback=callback)


def calc_rewards(rewards, num_episodes):
    time_now = datetime.now().strftime("%H:%M:%S")
    date_now = date.today()
    filename = "results/" + str(date_now) + \
        "-Keyboard-Agent-" + str(num_episodes) + \
        "-Episodes-" + str(time_now) + ".csv"

    timesteps = []
    for each in rewards:
        timesteps.append(len(each))

    file = open(filename, "w")
    for i in range(len(rewards)):
        file.write((str(sum(rewards[i])) + "," + str(timesteps[i])))
        file.write("\n")
    file.close()


play_game(num_episodes)
calc_rewards(rewards, num_episodes)
