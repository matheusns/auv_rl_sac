#!/usr/bin/env python3.8
import os
import rospy
import gymnasium as gym
from stable_baselines3 import SAC
from auv_rl_gym.task_envs.desistek_saga.auto_docking import AutoDocking

class PPOTrainer:
    def __init__(self, timesteps, log_dir):
        self.timesteps = timesteps
        self.env = gym.make('DesistekSagaAutoDocking-v0')
        self.model = SAC("MlpPolicy", 
                        self.env, verbose=2,
                        tensorboard_log=log_dir,
                        train_freq=(1,"episode"),
                        device="auto")

    def learn(self):
        self.model.learn(total_timesteps=self.timesteps)
    def save(self, path):
        self.model.save(path)
        vec_env = self.model.get_env()

if __name__ == "__main__":
    rospy.init_node('sac_trainer_node', anonymous=True, log_level=rospy.INFO)
    
    timesteps = rospy.get_param("/desistek_saga/sac/learn/timesteps")
    log_dir = rospy.get_param("/desistek_saga/sac/log/dir")
    save_dir = rospy.get_param("/desistek_saga/sac/log/save")
    model_name = rospy.get_param("/desistek_saga/sac/log/model_name")

    rospy.logdebug (f"timesteps = {timesteps}")
    rospy.logdebug (f"log_dir = {log_dir}")
    rospy.logdebug (f"save_dir = {save_dir}")
    rospy.logdebug (f"model_name = {model_name}")
    
    ppo = PPOTrainer(timesteps, log_dir)
    ppo.learn()
    ppo.save(os.path.join(save_dir, model_name))
    rospy.spin()