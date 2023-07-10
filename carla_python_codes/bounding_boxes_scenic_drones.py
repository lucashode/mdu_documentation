import carla
import math
import random
import time
import queue
import numpy as np
import cv2

def connect(world,camera_bp,image_queue,timeout = 5):
    t = time.time()
    while time.time()-t < timeout:
        try:
            id = world.get_actors().filter('*debris*')[0].id
            vehicle = world.get_actor(id)
            camera_init_trans = carla.Transform(carla.Location(x=2,z=2))
            camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)
            camera.listen(image_queue.put)
            # Get the world to camera matrix
            world_2_camera = np.array(camera.get_transform().get_inverse_matrix())
            # Get the attributes from the camera
            # Remember the edge pairs
            
            drone_civilian_ids = []
            if (world.get_actors().filter('*drone_civilian*'))!=[]:
                for drone in world.get_actors().filter('*drone_civilian*'):
                    drone_civilian_ids.append(drone.id)

            return id,vehicle,camera,world_2_camera,drone_civilian_ids
            
        except:
            pass
    print("Connection to scenic failed")
    exit(0)

def build_projection_matrix(w, h, fov):
    focal = w / (2.0 * np.tan(fov * np.pi / 360.0))
    K = np.identity(3)
    K[0, 0] = K[1, 1] = focal
    K[0, 2] = w / 2.0
    K[1, 2] = h / 2.0
    return K

def get_image_point(loc, K, w2c):
        # Calculate 2D projection of 3D coordinate

        # Format the input coordinate (loc is a carla.Position object)
        point = np.array([loc.x, loc.y, loc.z, 1])
        # transform to camera coordinates
        point_camera = np.dot(w2c, point)

        # New we must change from UE4's coordinate system to an "standard"
        # (x, y ,z) -> (y, -z, x)
        # and we remove the fourth componebonent also
        point_camera = [point_camera[1], -point_camera[2], point_camera[0]]

        # now project 3D->2D using the camera matrix
        point_img = np.dot(K, point_camera)
        # normalize
        point_img[0] /= point_img[2]
        point_img[1] /= point_img[2]

        return point_img[0:2]

client = carla.Client('localhost', 2000)
world  = client.get_world()
bp_lib = world.get_blueprint_library()

map = world.get_map().name[-6:]

#defining a timeout to scenic connection
scenic_timeout = 30


# defining camera attributes
camera_bp = bp_lib.find('sensor.camera.rgb')
camera_bp.set_attribute("image_size_x",str(640))
camera_bp.set_attribute("image_size_y",str(380))
camera_bp.set_attribute("fov",str(90))
camera_bp.set_attribute("sensor_tick",str(0.1))

image_w = camera_bp.get_attribute("image_size_x").as_int()
image_h = camera_bp.get_attribute("image_size_y").as_int()
fov = camera_bp.get_attribute("fov").as_float()
# Calculate the camera projection matrix to project from 3D -> 2D
K = build_projection_matrix(image_w, image_h, fov)


# Set up the simulator in synchronous mode
settings = world.get_settings()
settings.synchronous_mode = True # Enables synchronous mode
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

# Create a queue to store and retrieve the sensor data
image_queue = queue.Queue()


id,vehicle,camera,world_2_camera,drone_civilian_ids = connect(world,camera_bp,image_queue,scenic_timeout)


while True:
    
    

    # Process calculations only if a new image is available (enhance the simulator performance)
    while image_queue.empty():
        time.sleep(0.2)
        
    # Retrieve and reshape the image
    #camera.destroy()
    
    try:
        world.get_actors().filter('*debris*')[0].id
    except:
        camera.destroy()
        id,vehicle,camera,world_2_camera,drone_civilian_ids = connect(world,camera_bp,image_queue,scenic_timeout)
        

    image = image_queue.get()

    img = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4))

    # Get the camera matrix 
    world_2_camera = np.array(camera.get_transform().get_inverse_matrix())
                   
    for npc in world.get_actors().filter('*drone*'):

        # Filter out the ego vehicle
        
        if npc.id != vehicle.id:

            bb = npc.bounding_box
            dist = npc.get_transform().location.distance(vehicle.get_transform().location)

            # Filter for the vehicles within 50m
            if dist < 100:

            # Calculate the dot product between the forward vector
            # of the vehicle and the vector between the vehicle
            # and the other vehicle. We threshold this dot product
            # to limit to drawing bounding boxes IN FRONT OF THE CAMERA
                forward_vec = vehicle.get_transform().get_forward_vector()
                ray = npc.get_transform().location - vehicle.get_transform().location

                if forward_vec.dot(ray) > 1:
                    p1 = get_image_point(bb.location, K, world_2_camera)
                    verts = [v for v in bb.get_world_vertices(npc.get_transform())]
                    x_max = -10000
                    x_min = 10000
                    y_max = -10000
                    y_min = 10000

                    for vert in verts:
                        p = get_image_point(vert, K, world_2_camera)
                        # Find the rightmost vertex
                        if p[0] > x_max:
                            x_max = p[0]
                        # Find the leftmost vertex
                        if p[0] < x_min:
                            x_min = p[0]
                        # Find the highest vertex
                        if p[1] > y_max:
                            y_max = p[1]
                        # Find the lowest  vertex
                        if p[1] < y_min:
                            y_min = p[1]
                        
                    
                    
                    if npc.id in drone_civilian_ids:  
                           
                        cv2.line(img, (int(x_min),int(y_min)), (int(x_max),int(y_min)), (255,0,0, 255), 1)
                        cv2.line(img, (int(x_min),int(y_max)), (int(x_max),int(y_max)), (255,0,0, 255), 1)
                        cv2.line(img, (int(x_min),int(y_min)), (int(x_min),int(y_max)), (255,0,0, 255), 1)
                        cv2.line(img, (int(x_max),int(y_min)), (int(x_max),int(y_max)), (255,0,0, 255), 1)
                    else:
                        cv2.line(img, (int(x_min),int(y_min)), (int(x_max),int(y_min)), (255,0,122, 255), 1)
                        cv2.line(img, (int(x_min),int(y_max)), (int(x_max),int(y_max)), (255,0,122, 255), 1)
                        cv2.line(img, (int(x_min),int(y_min)), (int(x_min),int(y_max)), (255,0,122, 255), 1)
                        cv2.line(img, (int(x_max),int(y_min)), (int(x_max),int(y_max)), (255,0,122, 255), 1)

    for npc in world.get_actors().filter('*eagle_*'):

        # Filter out the ego vehicle
        
        if npc.id != vehicle.id:

            bb = npc.bounding_box
            dist = npc.get_transform().location.distance(vehicle.get_transform().location)

            # Filter for the vehicles within 50m
            if dist < 100:

            # Calculate the dot product between the forward vector
            # of the vehicle and the vector between the vehicle
            # and the other vehicle. We threshold this dot product
            # to limit to drawing bounding boxes IN FRONT OF THE CAMERA
                forward_vec = vehicle.get_transform().get_forward_vector()
                ray = npc.get_transform().location - vehicle.get_transform().location

                if forward_vec.dot(ray) > 1:
                    p1 = get_image_point(bb.location, K, world_2_camera)
                    verts = [v for v in bb.get_world_vertices(npc.get_transform())]
                    x_max = -10000
                    x_min = 10000
                    y_max = -10000
                    y_min = 10000

                    for vert in verts:
                        p = get_image_point(vert, K, world_2_camera)
                        # Find the rightmost vertex
                        if p[0] > x_max:
                            x_max = p[0]
                        # Find the leftmost vertex
                        if p[0] < x_min:
                            x_min = p[0]
                        # Find the highest vertex
                        if p[1] > y_max:
                            y_max = p[1]
                        # Find the lowest  vertex
                        if p[1] < y_min:
                            y_min = p[1]
                        
                     
                    cv2.line(img, (int(x_min),int(y_min)), (int(x_max),int(y_min)), (255,255,0, 255), 1)
                    cv2.line(img, (int(x_min),int(y_max)), (int(x_max),int(y_max)), (255,255,0, 255), 1)
                    cv2.line(img, (int(x_min),int(y_min)), (int(x_min),int(y_max)), (255,255,0, 255), 1)
                    cv2.line(img, (int(x_max),int(y_min)), (int(x_max),int(y_max)), (255,255,0, 255), 1)   


    cv2.imshow('ImageWindowName',img)
    if cv2.waitKey(1) == ord('q'):
        break


cv2.destroyAllWindows()
camera.destroy()
for npc in world.get_actors().filter('*vehicle*'):
    npc.destroy()

