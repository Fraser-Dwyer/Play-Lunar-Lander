import numpy as np
import gymnasium as gym
from gymnasium.utils.play import play, PlayPlot
import os
from datetime import datetime, date

num_of_episodes = 15   # Number of episodes to be played
nth = 4                # Save every nth episode
ep = 0                 # Current episode
episodes_to_save = list(range(num_of_episodes+1))
episodes_to_save = episodes_to_save[1::nth]
if (episodes_to_save[-1] == num_of_episodes):
    episodes_to_save[-1] = episodes_to_save[-1] - 1

ep_rew = []
rewards = []


def callback(obs_t, obs_tp1, action, rew, terminated, truncated, info):
    global rewards, ep_rew, ep, num_of_episodes
    ep_rew.append(rew)
    if terminated:
        ep += 1
        percent_done = ep*100 / num_of_episodes
        print("Episode: {:4.0f}    Reward: {:8.2f}    Percentage Complete: {:.2f}%".format(
            ep, sum(ep_rew), percent_done))
        rewards.append(ep_rew)
        ep_rew = []
    return [rew,]


def play_game(num_episodes, env):
    play(num_episodes, env, keys_to_action={
        "w": 2,
        "a": 1,
        "d": 3
    }, noop=0, callback=callback)


def calc_rewards(rewards, num_episodes, folder_name):
    filename = "results/" + folder_name + "/csv/cum_reward_and_timesteps.csv"

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


def run(num_of_episodes, episodes_to_save):
    print("\nKEYBOARD AGENT: {} EPISODE RUN \n".format(num_of_episodes))
    print("SAVING EPISODES: {}\n".format(episodes_to_save))
    time_now = datetime.now().strftime("%H:%M:%S")
    date_now = date.today()
    folder_name = str(date_now) + "-Keyboard-Agent-" + \
        str(num_of_episodes) + "-Episodes-" + str(time_now)
    os.mkdir("results/" + folder_name)
    os.mkdir("results/" + folder_name + "/recordings/")
    os.mkdir("results/" + folder_name + "/csv/")
    vid_dir = "results/" + folder_name + "/recordings/"

    # Make the environment
    env = gym.make("LunarLander-v2", render_mode="rgb_array")
    env = gym.wrappers.RecordVideo(
        env, vid_dir, episode_trigger=lambda x: x in episodes_to_save)

    play_game(num_of_episodes, env)
    calc_rewards(rewards, num_of_episodes, folder_name)


run(num_of_episodes, episodes_to_save)
