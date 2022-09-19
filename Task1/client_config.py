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

# block name
blueBlock = 'CuboidBlue'
greenBlock = 'CuboidGreen'
greenLakeBlock = 'CuboidGreenLake'
purpleBlock = 'CuboidPurple'
redBlock = 'CuboidRed'
whiteBlock = 'CuboidWhite'
yellowBlock = 'CuboidYellow'
posX = [0.35,0.275,0.35,-0.05,0.125,0.125,0.25]
posY = [0.025,0.2,-0.125,0.35,-0.35,0.325,-0.225]
posZ = [0.435,0.435,0.435,0.435,0.435,0.435,0.435]
oriA = [0,0,0,0,0,0,0]
oriB = [0,0,0,0,0,0,0]
oriG = [0,0,0,0,0,0,0]      
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

# Block handle
_, blueBlockHandle = vrep.simxGetObjectHandle(clientID,blueBlock,vrep.simx_opmode_oneshot_wait)
_, greenBlockHandle = vrep.simxGetObjectHandle(clientID,greenBlock,vrep.simx_opmode_oneshot_wait)
_, greenLakeBlockHandle = vrep.simxGetObjectHandle(clientID,greenLakeBlock,vrep.simx_opmode_oneshot_wait)
_, purpleBlockHandle = vrep.simxGetObjectHandle(clientID,purpleBlock,vrep.simx_opmode_oneshot_wait)
_, redBlockHandle = vrep.simxGetObjectHandle(clientID,redBlock,vrep.simx_opmode_oneshot_wait)
_, whiteBlockHandle = vrep.simxGetObjectHandle(clientID,whiteBlock,vrep.simx_opmode_oneshot_wait)
_, yellowBlockHandle = vrep.simxGetObjectHandle(clientID,yellowBlock,vrep.simx_opmode_oneshot_wait)

# read the angle of each joints
jointConfig = np.zeros((jointNum, 1))
for i in range(jointNum):
        _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_blocking)
        jointConfig[i] = jpos

# question for asking user input
userInput = ""
question = ""
inputHeading = ""

# input Status = ["setTarget"]
functionStatus = [0]
# setTarget Status = ["Joint1","Joint2","Joint3","Joint4","Joint5","Joint6"]
setTargetStatus = [0,0,0,0,0,0]
setTargetValue = [0.00,0.00,0.00,0.00,0.00,0.00]
setTargetQuestion = ["Please input the value of Base (Joint 1) in degree (deg): ","Please input the value of Shoulder (Joint 2) in degree (deg): ","Please input the value of Elbow (Joint 3) in degree (deg): ","Please input the value of Wrist 1 (Joint 4) in degree (deg): ","Please input the value of Wrist 2 (Joint 5) in degree (deg): ","Please input the value of Wrist 3 (Joint 6) in degree (deg): "]
