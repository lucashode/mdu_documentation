#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys
import random

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import math
import random
import time


def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    debug = world.debug
    
    # print(world.get_blueprint_library())
    drone_blueprint = world.get_blueprint_library().filter('static.prop.drone_civilian_phantom')
    print(drone_blueprint)
    spawn_point = world.get_map().get_spawn_points()[10]
    spawn_point.location.z = 10
    
    
        
        
    try:
        drone=world.spawn_actor(drone_blueprint[0],spawn_point) 
        id = drone.id
        print(world.get_actors())           
        drone.set_transform(carla.Transform(drone.get_location(),carla.Rotation(0,0,0)))
        roll=0
        yaw=0
        intensity = 5
        actual_yaw=0
        loop = False
        actual_pos = drone.get_location()
        while True:
            
            

            time.sleep(0.1)
            transform = drone.get_transform()
            if (roll,yaw) == (0,-1):
                if abs(abs(abs(transform.rotation.yaw)-actual_yaw)-90) <1:
                    roll,yaw = 0,0
                    actual_yaw = abs(transform.rotation.yaw)
                    
                    actual_pos = transform.location
                    loop=False
            elif (roll,yaw) == (-1,0):
                if abs(transform.rotation.roll) <1:
                    roll,yaw = 0,0
                    
                    actual_pos = transform.location
                    loop=True
            else:
                if transform.location.distance(actual_pos)>=50:
                    if loop==False:
                        roll,yaw = -1,0
                        intensity=10
                    else:
                        roll,yaw = 0,-1
                        intensity=5


            right_vect = transform.get_right_vector()
            drone.set_transform(carla.Transform(transform.location+right_vect,carla.Rotation(transform.rotation.pitch,transform.rotation.yaw+intensity*yaw,transform.rotation.roll+intensity*roll)))

            
            #print(drone.get_transform().rotation.roll)
            debug.draw_arrow(transform.location+right_vect,transform.location+4*(right_vect),thickness= 0.2,arrow_size=0.1,color=carla.Color(0,0,255),life_time=0.1)
            
    finally:
        print("\ndestroy drone")
        
        
        world.get_actor(id).destroy()
        exit(0)

if __name__ == '__main__':  

    main()
