# VTL_Basic-Collaborative-Robot
Basic-Collaborative-Robot is developed aiming to enable students to learn about the joints. Combining with some exercises to practice their controlling skill.

# NEWS
# 1. 20210817: UR3_IK_1708.ttt
## 1. Applied Inverse Kinematics
Using Kinematics Plugin to apply the inverse kinematics. There is a target and tip create for this model. The tip is located at the UR3_connection and under UR3_link7 at the list. There is a IK group to link up the tip and target which allows the UR3 to follow the target. 

## 2. Inverse Kinematics integrated with python remote API
Using the Python remote API to control the opening and closing of RG2 (Gripper). The target will lead the movement of UR3 and python program (TestingCoppeliaSim.py) aimed to control the gripper.

# 2. 20210831: Task1-2 (Task1)
## 1. Task 1: Welding with UR3
Using Python to control the UR3's end-effector to welding the plane shown on the table. The program transforms these planes from the camera location to the world location. After calculating the welding line by calculating the middle line between them. It can detect both horizontal and vertical lines.

## 2. Task 1.1: Welding Cross
Using the VREP's function "Path" to create the path which is the movement path of UR3. Combining with the Lua programming language, which the target will follow the path and welding the cross shape on the table. For the cross shape, the path is required to consider the z-axis.

## 3. Task 1.2: Welding my name
Almost the same with Task 1.1, because this task is more challenging. Since the shape is more complicated and larger, the position and orientation of path points are required to consider. It can prevent that UR3 weld another thing and occur collision.

## 4. Task 2: Choosing Cuboid and place it (Task2)
Using Python to control the whole task (UR3 movement, target position, and orientation, object position). Combining with the VREP camera filter, the camera can detect the red color object and return the camera-side position. The program will transform these positions into a world coordinate system and tell the UR3 to pick it.
One of the challenges is that student must set a waypoint which allows the UR3 to prevent the collision.

# 3. 20210903: Task3 (Task3)
## 1. Task 3: CNC Robot Arm
Using python to control the ur3 to complete some specific action (opening sliding door, closing the sliding door, picking the blocks from the rack, placing the block for processing, picking the block after processing, picking back the block to the rack). Students are required to practice the knowledge learned at the previous task. In the task, only some boxes(BoxID: 1, 2, 3, 4) can be completed. The remaining blocks will fail since the ur3 cannot reach their position. 
## 2. Error check
Function: 
checkOrientation(): used to check how close between the tip and target's orientation is. Also, it used to provide some delay for ur3's joints movement. Besides, it also can confirm the orientation before taking other action.

checkDistance(): it is just similar to the previous one.

# 4. 20210914: Digital Twins (vrep_urx)
To achieve the digital twins of the universal robot, this platform uses V-REP to design the scene and UR movement. URX is used to control the real universal robot.

# 1.1. Software Requirment
1. Ubuntu 18.04
2. V-REP 3.6.2 versions
3. Python 3.6

# 1.2. Start up Procedures
## 1. Downloading V-REP 3.6.2 versions
[https://www.coppeliarobotics.com/previousVersions]

## 2. pip3 installation
Step 1. update the system
`sudo apt-get update`

Step 2. Install pip3
`sudo apt-get -y install python3-pip`

Step 3. Verification
`pip3 --version`

## 3. install the following python library for further program execution.
```
import os
import cv2
import sys
import math
import time
import random
import string
import pygame
import sim
import numpy as np
```

Type the following command in the terminal for installing the python libraries

import cv2:
`pip3 install opencv-python`

import sys:
`pip3 install os-sys`

import pygame:
`sudo apt-get install python3-pygame`

# 1.3 Building CoppeliaSim-Python bridge (Python remote API)
Step 1. Find the following document in your coppeliaSim installation path.

sim.py & simConst.py & simpleTest.py: "YOUR_INSTALL_PATH/programming/remoteApiBindings/python/python"

remoteApi.so: "YOUR_INSTALL_PATH/programming/remoteApiBindings/lib/lib/Ubuntu18_04"

Step 2. Copying the above document in to your work place folder.

Step 3. Entering your coppeliaSim installation folder and opening the terminal. Excuting the following command for launching the coppeliaSim `./coppeliaSim.sh`
![image](https://github.com/Summer-Lo/VTL_Basic-Collaborative-Robot/blob/CoppeliaSim_v4.0.0/images/coppeliaSimExcutation.png)

Step 4. Opening the main script and typing the following command for building the connection. `simRemoteApi.start(19999)`
![image](https://github.com/Summer-Lo/VTL_Basic-Collaborative-Robot/blob/CoppeliaSim_v4.0.0/images/mainScript.png)


Step 5. Clicking the start button on the top tool bar first. Then open a new terminal in your work place folder and type `python3 simpleTest.py`. After that, it will output the current x position of your mouse in the coppeliaSim. It mean the connection is sucessful.
![image](https://github.com/Summer-Lo/VTL_Basic-Collaborative-Robot/blob/CoppeliaSim_v4.0.0/images/connection_successful.png)

# 2. Procedures for the program
Step 1 Find and pull the following objects at the left side list.
UR3 model:
![image](https://github.com/Summer-Lo/VTL_Basic-Collaborative-Robot/blob/CoppeliaSim_v4.0.0/images/ur3_location.png)
RG2 model:
![image](https://github.com/Summer-Lo/VTL_Basic-Collaborative-Robot/blob/CoppeliaSim_v4.0.0/images/rg2_location.png)

Step 2. Ctrl + left-click the UR3_connection and RG2 at the left-side menu bar. Then clicking the assemble/disassemble button to assemble these components.
![image](https://github.com/Summer-Lo/VTL_Basic-Collaborative-Robot/blob/CoppeliaSim_v4.0.0/images/assemble.png)

Step 3. Opening the rg2 child script. Then enter and replace the following command in the child script. The program is used to control the action of rg2, such as opening and closing. The following child script use Lua programming language to control. 
```
rg2Close = function(inInts,inFloats,inStrings,inBuffer)
    local v = -motorVelocity
    sim.setJointForce(motorHandle,motorForce)
    sim.setJointTargetVelocity(motorHandle,v)
    return {},{v},{},''
end

rg2Open = function(inInts,inFloats,inStrings,inBuffer)
    local v = motorVelocity
    sim.setJointForce(motorHandle,motorForce)
    sim.setJointTargetVelocity(motorHandle,v)
    return {},{v},{},''
end

function sysCall_init( )
    motorHandle=sim.getObjectHandle('RG2_openCloseJoint')
    motorVelocity=0.05 -- m/s
    motorForce=20 -- N
    rg2Open({}, {}, {}, '')
end
```

Step 4. Opening a terminal in your work place folder and typing the following command to excute the python program. `python3 TestingCoppeliaSim.py`
There are window disappeared which is used to control the simulation model by clicking keys.
![image](https://github.com/Summer-Lo/VTL_Basic-Collaborative-Robot/blob/CoppeliaSim_v4.0.0/images/controllingWindow.png)
The following table shows the keys and its corresponding action of different components.
```
    Q,W: joint 0
    A,S: joint 1
    Z,X: joint 2
    E,R: joint 3
    D,F: joint 4
    C,V: joint 5
    P: exit()
    T: close RG2
    Y: open RG2
    L: reset robot
    SPACE: save image
    T,Y: Gripper
```

# 3. Useful document
CoppeliaSim User Manual
[https://www.coppeliarobotics.com/helpFiles/index.html]

Remote API functions (Python)
[https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm]

Remote API functions (Lua)
[https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsLua.htm]

