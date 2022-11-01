import numpy as np
import math
import client_config as hc
import time
import vrep

global jointConfig
jointConfig = []

class data:
    RAD2DEG = 180 / math.pi

    def __init__(self):
        global jointConfig
        self.clientID = hc.clientID
        self.baseHandle = hc.baseHandle
        self.joint6Handle = hc.joint6Handle
        self.jointHandle = hc.jointHandle
        self.targetHandle = hc.targetHandle
        self.tipHandle = hc.tipHandle
        for i in range(len(self.jointHandle)):
            jointConfig.append(0)

    # Get and display the joint handle
    def getJointHandle(self):
        jointHandle = self.jointHandle
        #print(len(jointHandle))
        for n in range(len(jointHandle)):
            print("jointHandle",n,": ",jointHandle[n])

    # Get joint position in radius
    # Return the jointConfig
    def getJointPositionRadius(self):
        global jointConfig
        clientID = self.clientID
        jointHandle = self.jointHandle
        # for loop to display position in radius
        for i in range(len(jointHandle)):
            _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_blocking)                            # Get the specific joint joints
            jointConfig[i] = round(float(jpos), 4)
            print("Joint ",i," position: ",jointConfig[i]," rad")
        print('\n')
        return jointConfig

    # Get joint position in degree
    # Return the jointConfig
    def getJointPositionDegree(self):
        RAD2DEG = self.RAD2DEG
        clientID = self.clientID
        jointHandle = self.jointHandle
        for i in range(len(jointHandle)):
            _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_blocking)                            # Get the specific joint joints
            jointConfig[i] = round(float(jpos) * RAD2DEG, 2)
            #print("Joint ",i," position: ",jointConfig[i]," deg")
        #print('\n')
        return jointConfig

    # Get the end-effector position and orientation
    # Return the information
    def getTipInfomation(self):
        RAD2DEG = self.RAD2DEG
        clientID = self.clientID
        tipHandle = self.tipHandle
        _, position = vrep.simxGetObjectPosition(clientID, tipHandle, -1, vrep.simx_opmode_blocking)                            # Get the tip position
        _, orientaiton = vrep.simxGetObjectOrientation(clientID, tipHandle, -1, vrep.simx_opmode_blocking)                      # Get the tip orientation
        for i in range(3):
            orientaiton[i] = orientaiton[i] * RAD2DEG
        information = [0,0,0,0,0,0]
        for i in range(6):
            if (i <= 2):
                information[i] = round(position[i], 4)
            else:
                information[i] = round(orientaiton[i-3], 4)
        return information

'''
#testing
if __name__ == '__main__':
    test = data()
    test.getTargetInfomation()
'''
