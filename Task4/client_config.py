import vrep
import sys
import numpy as np


jointNum = 6
baseName = 'UR3'
rgName = 'RG2'
jointName = 'UR3_joint'
camera_rgb_Name = 'kinect_rgb'
camera_depth_Name = 'kinect_depth'
tipName = 'tip'
targetName = 'target'
pathName = 'Path'
visionSensorName = 'Vision_sensor'
camName = 'cam'
boxSensorName = 'boxSensor'
baseName0 = 'UR3#0'
rgName0 = 'RG2#0'
jointName0 = 'UR3_0joint'
tipName0 = 'tip#0'
targetName0 = 'target#0'
endingName = "#0"
#joint1Name = "UR3_joint1"
#joint2Name = "UR3_joint2"
#joint3Name = "UR3_joint3"
#joint4Name = "UR3_joint4"
#joint5Name = "UR3_joint5"
joint6Name = "UR3_joint6"

#jointNum = self.jointNum
#baseName = self.baseName
#rgName = self.rgName
#jointName = self.jointName
#camera_rgb_Name = self.camera_rgb_Name
#camera_depth_Name = self.camera_depth_Name
#tipName = self.tipName
#targetName = self.targetName
#pathName = self.pathName
#visionSensorName = self.visionSensorName
#camName = self.camName
        
print('Simulation started')

try:
    
    vrep.simxFinish(-1) #close the previous connections
    clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
    if clientID!=-1:
        print ('connect successfully')
    else:
        sys.exit("Error: no se puede conectar") #Terminar este script

except:
    print('Check if CoppeliaSim is open')


vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)     #Start simulation
print("Simulation start")




# Read the handle of Base and Joints
jointHandle = [0,0,0,0,0,0]
for i in range(jointNum):
    _, returnHandle = vrep.simxGetObjectHandle(clientID, jointName + str(i+1), vrep.simx_opmode_blocking)
    jointHandle[i] = returnHandle

jointHandle0 = [0,0,0,0,0,0]
for i in range(jointNum):
    _, returnHandle = vrep.simxGetObjectHandle(clientID, jointName + str(i+1) + endingName, vrep.simx_opmode_blocking)
    jointHandle0[i] = returnHandle

#initization
_, baseHandle = vrep.simxGetObjectHandle(clientID, baseName, vrep.simx_opmode_blocking)
_, rgHandle = vrep.simxGetObjectHandle(clientID, rgName, vrep.simx_opmode_blocking)
_, cameraRGBHandle = vrep.simxGetObjectHandle(clientID, camera_rgb_Name, vrep.simx_opmode_blocking)
_, cameraDepthHandle = vrep.simxGetObjectHandle(clientID, camera_depth_Name, vrep.simx_opmode_blocking)
_, tipHandle = vrep.simxGetObjectHandle(clientID, tipName, vrep.simx_opmode_blocking)
_, targetHandle = vrep.simxGetObjectHandle(clientID, targetName, vrep.simx_opmode_blocking)
_, pathHandle = vrep.simxGetObjectHandle(clientID, pathName, vrep.simx_opmode_blocking)
_, visionSensorHandle = vrep.simxGetObjectHandle(clientID,visionSensorName,vrep.simx_opmode_oneshot_wait)
_, camHandle = vrep.simxGetObjectHandle(clientID,camName,vrep.simx_opmode_oneshot_wait)
_, boxSensorHandle = vrep.simxGetObjectHandle(clientID,boxSensorName,vrep.simx_opmode_oneshot_wait)
#_, joint1Handle = vrep.simxGetObjectHandle(clientID,joint1Name,vrep.simx_opmode_oneshot_wait)
#_, joint2Handle = vrep.simxGetObjectHandle(clientID,joint2Name,vrep.simx_opmode_oneshot_wait)
#_, joint3Handle = vrep.simxGetObjectHandle(clientID,joint3Name,vrep.simx_opmode_oneshot_wait)
#_, joint4Handle = vrep.simxGetObjectHandle(clientID,joint4Name,vrep.simx_opmode_oneshot_wait)
#_, joint5Handle = vrep.simxGetObjectHandle(clientID,joint5Name,vrep.simx_opmode_oneshot_wait)
_, joint6Handle = vrep.simxGetObjectHandle(clientID,joint6Name,vrep.simx_opmode_oneshot_wait)

_, baseHandle0 = vrep.simxGetObjectHandle(clientID, baseName0, vrep.simx_opmode_blocking)
_, rgHandle0 = vrep.simxGetObjectHandle(clientID, rgName0, vrep.simx_opmode_blocking)
_, tipHandle0 = vrep.simxGetObjectHandle(clientID, tipName0, vrep.simx_opmode_blocking)
_, targetHandle0 = vrep.simxGetObjectHandle(clientID, targetName0, vrep.simx_opmode_blocking)
# read the angle of each joints
jointConfig = np.zeros((jointNum, 1))
for i in range(jointNum):
        _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_blocking)
        jointConfig[i] = jpos
jointConfig0 = np.zeros((jointNum, 1))
for i in range(jointNum):
        _, jpos = vrep.simxGetJointPosition(clientID, jointHandle0[i], vrep.simx_opmode_blocking)
        jointConfig0[i] = jpos
