import numpy as np
import math
import client_config as hc
import time
import vrep

global jointConfig, jointConfig0
jointConfig = []
jointConfig0 = []

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
        self.baseHandle0 = hc.baseHandle0
        self.jointHandle0 = hc.jointHandle0
        self.targetHandle0 = hc.targetHandle0
        self.tipHandle0 = hc.tipHandle0
        for i in range(len(self.jointHandle)):
            jointConfig.append(0)
        for i in range(len(self.jointHandle0)):
            jointConfig0.append(0)

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
            _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_blocking)
            jointConfig[i] = round(float(jpos), 4)
            #print("Joint ",i," position: ",jointConfig[i]," rad")
        #print('\n')
        return jointConfig

    # Get joint position in degree
    # Return the jointConfig
    def getJointPositionDegree(self):
        RAD2DEG = self.RAD2DEG
        clientID = self.clientID
        jointHandle = self.jointHandle
        for i in range(len(jointHandle)):
            _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_blocking)
            jointConfig[i] = round(float(jpos) * RAD2DEG, 2)
            #print("Joint ",i," position: ",jointConfig[i]," deg")
        #print('\n')
        #print(jointConfig)
        return jointConfig

    def getTargetInfomation(self):
        RAD2DEG = self.RAD2DEG
        clientID = self.clientID
        tipHandle = self.tipHandle
        _, position = vrep.simxGetObjectPosition(clientID, tipHandle, -1, vrep.simx_opmode_blocking)
        _, orientaiton = vrep.simxGetObjectOrientation(clientID, tipHandle, -1, vrep.simx_opmode_blocking)
        for i in range(3):
            orientaiton[i] = orientaiton[i] * RAD2DEG
        information = [0,0,0,0,0,0]
        for i in range(6):
            if (i <= 2):
                information[i] = round(position[i], 4)
            else:
                information[i] = round(orientaiton[i-3], 4)
        information[2] = round((float(information[2]) - 0.41),4)
        return information
    
    def getJoint0PositionDegree(self):
        RAD2DEG = self.RAD2DEG
        clientID = self.clientID
        jointHandle0 = self.jointHandle0
        #print(jointHandle0)
        for i in range(len(jointHandle0)):
            _, jpos = vrep.simxGetJointPosition(clientID, jointHandle0[i], vrep.simx_opmode_blocking)
            #print(jpos)
            jointConfig0[i] = round(float(jpos) * RAD2DEG, 2)
            #print("Joint ",i," position: ",jointConfig0[i]," deg")
        #print('\n')
        #print(jointConfig)
        return jointConfig0

    def getTarget0Infomation(self):
        RAD2DEG = self.RAD2DEG
        clientID = self.clientID
        tipHandle0 = self.tipHandle0
        _, position = vrep.simxGetObjectPosition(clientID, tipHandle0, -1, vrep.simx_opmode_blocking)
        _, orientaiton = vrep.simxGetObjectOrientation(clientID, tipHandle0, -1, vrep.simx_opmode_blocking)
        for i in range(3):
            orientaiton[i] = orientaiton[i] * RAD2DEG
        information = [0,0,0,0,0,0]
        for i in range(6):
            if (i <= 2):
                information[i] = round(position[i], 4)
            else:
                information[i] = round(orientaiton[i-3], 4)
        information[0] = round(float(information[0]),4)
        information[2] = round((float(information[2]) - 0.41),4)
        #print(information)
        return information

'''
#testing
if __name__ == '__main__':
    test = data()
    test.getJoint0PositionDegree()
    test.getJointPositionDegree()
'''
