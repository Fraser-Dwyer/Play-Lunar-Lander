import numpy as np
import gymnasium as gym
from gymnasium.utils.play import play, PlayPlot

from datetime import datetime, date

num_episodes = 11
ep = 0
env = gym.make("LunarLander-v2", render_mode="rgb_array")

ep_rew = []
rewards = []


def callback(obs_t, obs_tp1, action, rew, terminated, truncated, info):
    global rewards, ep_rew, ep, num_episodes
    ep_rew.append(rew)
    if terminated:
        ep += 1
        percent_done = ep*100 / num_episodes
        print("Episode: {:4.0f}    Reward: {:8.2f}    Percentage Complete: {:.2f}%".format(
            ep, sum(ep_rew), percent_done))
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

    total_rewards = 0
    total_time = 0

    timesteps = []
    for each in rewards:
        timesteps.append(len(each))

    file = open(filename, "w")
    for i in range(len(rewards)):
        total_rewards += sum(rewards[i])
        total_time += timesteps[i]
        file.write((str(sum(rewards[i])) + "," + str(timesteps[i])))
        file.write("\n")
    file.close()

    print("\nSUMMARY:\n - Average Reward      {:.2f}    \n - Average Timesteps   {:.2f}".format(
        total_rewards/num_episodes, total_time/num_episodes))


print("\nKEYBOARD AGENT: {} EPISODE RUN \n".format(num_episodes))
play_game(num_episodes)
calc_rewards(rewards, num_episodes)
