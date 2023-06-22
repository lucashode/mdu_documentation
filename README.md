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
Scenic is a scenario generator that works with Carla. First install the scenic branch we did : 
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

### Add custom assets to Carla

In this part I'll suppose that the package that contains the assets you want is already cooked. If you want to learn about that, refers to the Carla documentation.

To import assets or map, you'll just need to put the package in the Import folder of the Carla repository and run in the bash :
```bash
./ImportAssets.sh
```
This should create a new folder in the carla/CarlaUE4/Content/

#### Maps 

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





