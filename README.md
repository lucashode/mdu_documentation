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
