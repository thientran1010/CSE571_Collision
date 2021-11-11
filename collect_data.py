# ************** STUDENTS EDIT THIS FILE **************

from SteeringBehaviors import Wander
import SimulationEnvironment as sim
import pygame, sys

import numpy as np
import pandas as pd
def collect_training_data(total_actions):
    #set-up environment
    sim_env = sim.SimulationEnvironment()

    #robot control
    action_repeat = 100
    steering_behavior = Wander(action_repeat)

    num_params = 7
    #STUDENTS: network_params will be used to store your training data
    # a single sample will be comprised of: sensor_readings, action, collision
    x1,x2,x3,x4,x5,a,y = 0,0,0,0,0,0,0;
    sensor_readings = list
    action = int
    collision = int
    network_params = {sensor_readings, action, collision}
    
    df = pd.DataFrame(columns=['s1', 's2', 's3','s4','s5','action','collision'])
    index = 0

    for action_i in range(total_actions):
        for event in pygame.event.get():
            pass
        progress = 100*float(action_i)/total_actions
        #print(f'Collecting Training Data {progress}%   ', end="\r", flush=True)
        

        #steering_force is used for robot control only
        action, steering_force = steering_behavior.get_action(action_i, sim_env.robot.body.angle)
        #print('action:' , action)
        for action_timestep in range(action_repeat):
            row=list()
            if action_timestep == 0:
                
                state, collision, sensor_readings = sim_env.step(steering_force)
                #State 
                # print('act1: ')
                # print('state:', state)
                # print('collisiontop: ', collision)
                # print('sensor', sensor_readings)
                # print('sensor', type(sensor_readings))
                # print(sensor_readings[0])
                
            else:
                state, collision, sensor_readings = sim_env.step(steering_force)
                # print('act2: ')
                # print('state:', state)
                # print('collisiontop: ', collision)
                # print('sensor', sensor_readings)
                #print(a,b)
               
            
            
            
            if collision:
                #print("collision_warning: ",collision)
                steering_behavior.reset_action()
                #STUDENTS NOTE: this statement only EDITS collision of PREVIOUS action
                #if current action is very new.
                if action_timestep < action_repeat * .3: #in case prior action caused collision
                    #print("collision_bottom: ",collision)
                    #To do:
                    df.iloc[-1, df.columns.get_loc('collision')] = collision
                    #print(df.iloc[-1])
                    #network_params[-1][-1] = collision #share collision result with prior action
                break
        row = list()
        row.extend(sensor_readings.tolist())
        row.append(action)
        row.append(collision)
        # print('row: ', row)
        row = pd.Series(row, index = df.columns)
        if(len(row)!=0):
            if(index<(40000)):
                df = df.append(row,ignore_index=True)
                index = index+1
            elif(row['collision']==1):
                df = df.append(row,ignore_index=True)
                index = index+1
        # if((len(df)%2000) == 0):
        #     df.to_csv('submission2.csv',header=False,mode='a',index=False,line_terminator='\n')
        #     lst = [df]
        #     del lst
        #     df = pd.DataFrame(columns=['s1', 's2', 's3','s4','s5','action','collision'])
        #     index = 0
        if(index>80000):
            break
        
    #print(df.head(100))
    df.to_csv('submission2.csv',header=False,mode='a',index=False,line_terminator='\n')


        #STUDENTS: Update network_params.


    #STUDENTS: Save .csv here. Remember rows are individual samples, the first 5
    #columns are sensor values, the 6th is the action, and the 7th is collision.
    #Do not title the columns. Your .csv should look like the provided sample.








if __name__ == '__main__':
    total_actions = 80000
    collect_training_data(total_actions)
