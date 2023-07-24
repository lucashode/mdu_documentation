# mdu_documentation
This document is a feedback on everything we've been through for the mdu_carla project. 

## Computer configuration
* CPU : Intel® Xeon(R) Silver 4210R CPU @ 2.40GHz × 8
* GPU : NVIDIA RTX A5000
* 16gb RAM
* Ubuntu 18.04
* Python 3.8.16

## Installation of Carla
For the installation of Carla 0.9.14 we followed the Carla's documentation :
https://carla.readthedocs.io/en/latest/
After the installation of everything do : 
```bash
./CarlaUE4.sh
```
This should open a Carla window.

If you use Carla in a vm, the sensitivity should be way too high. To avoid this problem, in carla/CarlaUE4/Config/DefaultInput.ini add those few lines :

```bash
-AxisConfig=(AxisKeyName="MouseX",AxisProperties=(DeadZone=0.00000,Exponent=1.00000,Sensitivity=0.300,Scale=-1.0000))
-AxisConfig=(AxisKeyName="MouseY",AxisProperties=(DeadZone=0.00000,Exponent=1.00000,Sensitivity=0.300,Scale=-1.0000))
+AxisConfig=(AxisKeyName="MouseX",AxisProperties= (DeadZone=0.000000,Sensitivity=0.3000,Scale=1.0000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MouseY",AxisProperties=(DeadZone=0.000000,Sensitivity=0.3000,Scale=1.0000,Exponent=1.000000,bInvert=False))
bUseMouseForTouch=True
bEnableMouseSmoothing=False
```

## Python API
To start using Carla the first thing is to create a python virtual environment and do :
```bash
pip import carla
```

* From there you can try the : 
```bash
python carla/PythonAPI/examples/generate_traffic.py
```
This should generate some cars/pedestrians on the carla world and make them drive.
* You can also try the :
```bash
python carla/PythonAPI/examples/manual_control.py
```
To control the car in the map.

* You can also use the config.py file that allows you to have a better control of the Carla client.
```bash
cd carla/PythonAPI/util
./config.py -h
```

## Scenic
### Installation
Scenic is a scenario generator that works with Carla. We used the scenic 2 version because scenic 3 wasn't released officially. First install the scenic branch we did : 
```bash
git clone github.com/lucashode/Scenic
```
This folder contains all the changes I've done, especially for the drones.
You'll also need to install every python requirements, preferably in a virtual environment.
```bash
pip install scenic
```

### Learning Scenic
To learn scenic syntax, I advise to :
1. Read the Scenic documentation : https://scenic-lang.readthedocs.io/en/latest/
2. Read the following document : https://link.springer.com/article/10.1007/s10994-021-06120-5
3. Check the examples in the Scenic repositories

To run a simulation in Carla you need to respect the following conditions :

1. In the scenic script you want to use, you need to precise in the first lines :
   ```bash
   param carla_map = 'path/to/the/map.xodr'
   param map = 'map.xodr'
   scenic.simulators.carla.model
   ```
2. Then in the bash :
   ```bash
   scenic script.scenic --simulate
   ```

This should open a pygame window that runs the scenario you want. 

You can add some parameters in the prompt to control better the simulation such as :
* ```bash
   scenic script.scenic --simulate --time 200
   ```
That will start a new simulation after 200 world ticks

* ```bash
   scenic script.scenic --simulate --count 5
   ```
That will stop generating new simulations after 5 successful simulations

## Add custom assets to Carla

In this part I'll suppose that the package that contains the assets you want is already cooked. If you want to learn about that, refers to the Carla documentation.

To import assets or map, you'll just need to put the package in the Import folder of the Carla repository and run in the bash :
```bash
./ImportAssets.sh
```
This should create a new folder in the carla/CarlaUE4/Content/

### Maps 

If the asset is a map, to check if it's well imported, open the Carla server then run the config.py in the bash :
```bash
cd carla/PythonAPI/util
./config.py --list
```

This should print the available weather/maps. 
Find your custom map then :  
```bash
./config.py --map Custom_map
```
This should open your map in the Carla window.

You can then try to generate traffic to see if the map works well.

* If you want to use it with scenic :
1. Take the file from carla/CarlaUE4/Content/Custom_map/Maps/Custom_map/Opendrive/Custom_map.xodr to Scenic/tests/formats/maps/opendrive/maps/Carla/
    
2. Then in your scenic code :
   ```bash
   param carla_map = 'path/to/the/Custom_map.xodr'
   param map = 'Custom_map.xodr'
   scenic.simulators.carla.model
   ```

Then the simulation should start on the custom map.

### Props

If the asset is a prop, to check if it's well imported, open the Carla server then in a python script, find your asset in the blueprint library like that:
  ```bash
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    print(world.get_blueprint_library())
   ```
Once you find it, you can use the spawn_actor method :

  ```bash
    spawn_point = world.get_map().get_spawn_points()[0]
    custom_asset_bp = world.get_blueprint_library().filter('name_of_the_bp')
    custom_asset=world.spawn_actor(custom_asset_bp,spawnpoint) 
   ```
If the prop is well imported, it should spawn on the Carla server.

##### Else, you can try to check multiple things to fix the problem :
1. Restart the Carla server. Indeed, especially if you import the assets while a Carla instance was already up, you should restart the server to apply changes.
2. Check the json file of the asset. In carla/CarlaUE4/Content/YourPackage/Config you should find a json file that shows all the assets added with package. An example of an asset in the json file should look like this :
   ```
        {
            "name": "asset01",
            "path": "/Game/YourPackage/Static/Dynamic/asset_01/asset_01.asset_01",
            "size": "tiny"
        }
   ```
What you have to check is that the path really refers to an existing file. To do that, follow the path and try to find asset_01.uexp & asset_01.uasset. If those don't exist, then try to find one whose name is close (for example asset_01_diff). Therefore modify the json file:
```
        {
            "name": "asset01",
            "path": "/Game/YourPackage/Static/Dynamic/asset_01/asset_01_diff.asset_01_diff",
            "size": "tiny"
        }
   ```
Then restart the server and try to spawn actor again.
This issue came from the naming of the different part of the assets in the fbx file so you should be really careful about the assets you use.

3. If after this check it still doesn't work then it's probably the fault of the fbx file you tried to import so you should go back to blender and check about the asset.

#### Add props assets in Scenic

To use your custom assets with Scenic, follow those steps :

1. Go to Scenic/src/scenic/simulators/carla/blueprints.scenic
2. Find "## Prop blueprints"
3. Add a new category of props like that :
```
   #: blueprints for custom assets
customAssetModels = [
      'static.prop.asset01',
      'static.prop.asset02',
      ...
      'static.prop.assetxx'
]
```
4. Then in the same repository open model.scenic
5. Create a new class derivated from the prop class like that :
```
class CustomAssets(Prop):
    blueprint: Uniform(*blueprints.customAssetModels)
```
6. Then you can spawn the custom asset by writing in a scenic script :
```
customaAsset = CustomAsset
```

## Drones assets

In this section I will explain how we implemented drones in Carla and Scenic through the following steps :

1. Spawn the drones in Carla with its Python API
2. Control the drones with Python
3. Spawn the drones with Scenic
4. Control the Scenic created drones with Python
5. Control the drones with Scenic
   
* The spawn of the drones was just an application of the previous section with drone models we found on internet.
* To control them I wrote a python script that could make the drone move forward, turn right and do a looping. 
* To spawn the drone with scenic we first followed the method previously presented. But then we faced the problem of elevation. Indeed, Scenic is a 2D scenario generator, so we needed to make adjustments to make it spawn things in the Carla 3D world.
      * In Scenic/src/scenic/simulators/carla/simulator.py modify : 
```
loc = utils.scenicToCarlaLocation(obj.position, world=self.world, blueprint=obj.blueprint)
```
To
```
loc = utils.scenicToCarlaLocation(obj.position,obj.elevation, world=self.world, blueprint=obj.blueprint)
```
Those changes are already done on our Scenic branch.
Then to spawn the drone you just need to write in a Scenic script :
```
drone = Drone with elevation 10
```

*	To control the Scenic drone with Carla’s Python API :
      1.	Start the Scenic simulation that create a drone. 
      2.	Start a Python Script that find the drone between all the actors on the server
      3.	Make this actor move with the python script previously written

The script "drone_with_scenic" does that.  
The result is the following : 
<p align="center">
  <img src="images/drone_scenic_python.gif?raw=true" alt="Bounding boxes" style="width:600px;"/>
</p>

*	To control the Scenic drone with Scenic only, I needed to create Actions and Behaviors for the drone. Go to Scenic/src/scenic/simulators/carla/
      * In actions.py : I created basic actions such as go forward, turn right, and turn left. 
      * In behaviors.scenic : I created a drone behavior that would make the drone go forward and turn left or right after a defined amount of time
      * Those actions/behaviors can be found in our Scenic branch.

Once everything is defined, in a Scenic script write : 
```
drone = Drone with elevation 10, with behavior DroneBehavior
```
This should spawn a moving drone 10 meters above the road

### Military & Civilian Drones

One of the project we had was to create a dataset with different type of Drones, with the most important categories : Military and Civilian Drones.  
To implement them I just created 2 new classes of blueprints that would contain the civilian/militarian drone models.  
```
#: blueprints for drones
civiliandroneModels = [
      'static.prop.drone_civilian_parrot',
      'static.prop.drone_civilian_minimalistic',
      'static.prop.drone_civilian_generic',
      'static.prop.drone_civilian_phantom',
]

#: blueprints for drones
militarydroneModels = [
      'static.prop.drone_f35',
      'static.prop.drone_military_bayraktar',
      'static.prop.drone_fictitious_cyberpolicevtol',
      'static.prop.drone_military_reaper'
]
```
I also added 2 new models classes that derivate from the Drone class : 
```
class Drone(Prop):
    regionContainedIn: road
    position: Point on road
    heading: Range(0, 360) deg
    width: 0.5
    length: 0.5
    physics: False

class CivilianDrone(Drone):
    blueprint: Uniform(*blueprints.civiliandroneModels)

class MilitaryDrone(Drone):
    blueprint: Uniform(*blueprints.militarydroneModels)
```

This way we can spawn Military/Civilian Drones and gave them the DroneBehavior.

By the way this is expendable for new kinds of flying objects like birds for examples.

## Bounding Boxes and Labelling

One of the objectives of this project was to generate datasets to train machine learning models. To do so, we need labelled images, with the position of every important objects on the image. 

The advantage of carla is that it can generate the images and the labels automatically.  
To do that I followed this tutorial on the Carla documentation : https://carla.readthedocs.io/en/latest/tuto_G_bounding_boxes/

### With Python API

The script "bounding_boxes.py" is a basic application of this tutorial.
1. It first create a car and place a camera on it and make it drive.
2. It creates 50 other cars and make them all drive.
3. Every sensor_ticks, the script gets a new image from the camera
4. Finally it draws bounding boxes around cars(blue), traffic signs(yellow), traffic_lights in two variations, white if the car can't know its color, magenta else.  
The result is the following : 
<p align="center">
  <img src="images/bounding_boxes.gif?raw=true" alt="Bounding boxes" style="width:600px;"/>
</p>

The "generate_xml.py" does the same but exports the images and the bounding boxes in Pascal VOC Format. With that, it is possible to create datasets.

### Adding Scenic

To make it usable with Drones, the objective was to be able to start a scenario with Scenic and use Python to connect to the simulation.  
The script "bounding_boxes_scenic_drones" is what I've done to answer this issue. It has to work with "drone.scenic".
What he does is quite simple : 
1. Connect to the Carla world
2. Setup the cameras
3. Find the ego thing (which is a debris)
4. Stick a camera to it
5. Get images and draw the bounding boxes around objects until the camera is destroyed (because the scenic simulation is finished)
6. Try to find the ego thing again
   




