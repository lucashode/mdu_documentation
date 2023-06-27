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

def connect(world,timeout = 5):
    t = time.time()
    while time.time()-t < timeout:
        try:
            id = world.get_actors().filter('static.prop.f35')[0].id
            return id
        except:
            pass
    print("Connection to scenic failed")
    exit(0)
    


def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    

    spawn_point = world.get_map().get_spawn_points()[10]
    spawn_point.location.z = 10

    scenic_timeout = 10

    id = connect(world,scenic_timeout)

    print("Connection to scenic achieved !")

    drone = world.get_actor(id) 

    

    drone.set_transform(carla.Transform(drone.get_location(),carla.Rotation(0,0,0)))
    
    roll=0
    yaw=0
    intensity = 5
    actual_yaw=0
    loop = False
    actual_pos = drone.get_location()
    while True:
        try:
            world.get_actors().filter('static.prop.f35')[0].id
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
            drone.set_transform(carla.Transform(transform.location+right_vect,carla.Rotation(yaw = transform.rotation.yaw+intensity*yaw,roll = transform.rotation.roll+intensity*roll)))

        except:
            print("Simulation ended")
            exit(0)

if __name__ == '__main__':

    main()
