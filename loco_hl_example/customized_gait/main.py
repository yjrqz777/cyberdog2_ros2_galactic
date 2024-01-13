'''
This demo show the communication interface of MR813 motion control board based on Lcm
- robot_control_cmd_lcmt.py
- file_send_lcmt.py
- Gait_Def_moonwalk.toml
- Gait_Params_moonwalk.toml
- Usergait_List.toml
'''
import lcm
import sys
import time
import toml
import copy
import math
from robot_control_cmd_lcmt import robot_control_cmd_lcmt
from file_send_lcmt import file_send_lcmt

robot_cmd = {
    'mode':0, 'gait_id':0, 'contact':0, 'life_count':0,
    'vel_des':[0.0, 0.0, 0.0],
    'rpy_des':[0.0, 0.0, 0.0],
    'pos_des':[0.0, 0.0, 0.0],
    'acc_des':[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'ctrl_point':[0.0, 0.0, 0.0],
    'foot_pose':[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'step_height':[0.0, 0.0],
    'value':0,  'duration':0
    }

def main():
    lcm_cmd = lcm.LCM("udpm://239.255.76.67:7671?ttl=255")
    lcm_usergait = lcm.LCM("udpm://239.255.76.67:7671?ttl=255")
    usergait_msg = file_send_lcmt()
    cmd_msg = robot_control_cmd_lcmt()
    try:
        steps = toml.load("Gait_Params_moonwalk.toml")
        full_steps = {'step':[robot_cmd]}
        k =0
        for i in steps['step']:
            cmd = copy.deepcopy(robot_cmd)
            cmd['duration'] = i['duration']
            if i['type'] == 'usergait':                
                cmd['mode'] = 11 # LOCOMOTION
                cmd['gait_id'] = 110 # USERGAIT
                cmd['vel_des'] = i['body_vel_des']
                cmd['rpy_des'] = i['body_pos_des'][0:3]
                cmd['pos_des'] = i['body_pos_des'][3:6]
                cmd['foot_pose'][0:2] = i['landing_pos_des'][0:2]
                cmd['foot_pose'][2:4] = i['landing_pos_des'][3:5]
                cmd['foot_pose'][4:6] = i['landing_pos_des'][6:8]
                cmd['ctrl_point'][0:2] = i['landing_pos_des'][9:11]
                cmd['step_height'][0] = math.ceil(i['step_height'][0] * 1e3) + math.ceil(i['step_height'][1] * 1e3) * 1e3
                cmd['step_height'][1] = math.ceil(i['step_height'][2] * 1e3) + math.ceil(i['step_height'][3] * 1e3) * 1e3
                cmd['acc_des'] = i['weight']
                cmd['value'] = i['use_mpc_traj']
                cmd['contact'] = math.floor(i['landing_gain'] * 1e1)
                cmd['ctrl_point'][2] =  i['mu']
            if k == 0:
                full_steps['step'] = [cmd]
            else:
                full_steps['step'].append(cmd)
            k=k+1
        f = open("Gait_Params_moonwalk_full.toml", 'w')
        f.write("# Gait Params\n")
        f.writelines(toml.dumps(full_steps))
        f.close()

        file_obj_gait_def = open("Gait_Def_moonwalk.toml",'r')
        file_obj_gait_params = open("Gait_Params_moonwalk_full.toml",'r')
        usergait_msg.data = file_obj_gait_def.read()
        lcm_usergait.publish("user_gait_file",usergait_msg.encode())
        time.sleep(0.5)
        usergait_msg.data = file_obj_gait_params.read()
        lcm_usergait.publish("user_gait_file",usergait_msg.encode())
        time.sleep(0.1)
        file_obj_gait_def.close()
        file_obj_gait_params.close()

        user_gait_list = open("Usergait_List.toml",'r')
        steps = toml.load(user_gait_list)
        for step in steps['step']:
            cmd_msg.mode = step['mode']
            cmd_msg.value = step['value']
            cmd_msg.contact = step['contact']
            cmd_msg.gait_id = step['gait_id']
            cmd_msg.duration = step['duration']
            cmd_msg.life_count += 1
            for i in range(3):
                cmd_msg.vel_des[i] = step['vel_des'][i]
                cmd_msg.rpy_des[i] = step['rpy_des'][i]
                cmd_msg.pos_des[i] = step['pos_des'][i]
                cmd_msg.acc_des[i] = step['acc_des'][i]
                cmd_msg.acc_des[i+3] = step['acc_des'][i+3]
                cmd_msg.foot_pose[i] = step['foot_pose'][i]
                cmd_msg.ctrl_point[i] = step['ctrl_point'][i]
            for i in range(2):
                cmd_msg.step_height[i] = step['step_height'][i]
            lcm_cmd.publish("robot_control_cmd",cmd_msg.encode())
            time.sleep( 0.1 )
        for i in range(75): #15s Heat beat It is used to maintain the heartbeat when life count is not updated
            lcm_cmd.publish("robot_control_cmd",cmd_msg.encode())
            time.sleep( 0.2 )
    except KeyboardInterrupt:
        cmd_msg.mode = 7 #PureDamper before KeyboardInterrupt:
        cmd_msg.gait_id = 0
        cmd_msg.duration = 0
        cmd_msg.life_count += 1
        lcm_cmd.publish("robot_control_cmd",cmd_msg.encode())
        pass
    sys.exit()

if __name__ == '__main__':
    main()
