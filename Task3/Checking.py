import numpy as np
import math
import time
import client_config as hc
import time
import vrep


class Check:
    RAD2DEG = 180 / math.pi

    def __init__(self):
        self.jointConfig = hc.jointConfig
        self.clientID = hc.clientID
        self.baseHandle = hc.baseHandle
        self.targetHandle = hc.targetHandle
        self.tipHandle = hc.tipHandle


    # Check the distance between target and end-effector
    # The smaller value represent to closer with each other
    def checkDistance (self,factor):
        clientID = self.clientID
        targetHandle = self.targetHandle
        tipHandle = self.tipHandle
        returnCode1 = 1
        returnCode2 = 1
        while(returnCode1==1 and returnCode2==1):
            returnCode1,targetPosition = vrep.simxGetObjectPosition(clientID, targetHandle, -1, vrep.simx_opmode_blocking)
            returnCode2,tipPosition = vrep.simxGetObjectPosition(clientID, tipHandle, -1, vrep.simx_opmode_blocking)
            print(returnCode1)
            print(returnCode2)
            #print(targetPosition[0],tipPosition[0])
            #print(targetPosition[1],tipPosition[1])
            #print(targetPosition[2],tipPosition[2])
            distance = math.sqrt(pow(abs(targetPosition[0]-tipPosition[0]),2)+pow(abs(targetPosition[1]-tipPosition[1]),2)+pow(abs(targetPosition[2]-tipPosition[2]),2))
        print(distance)
        #print(type(distance))
        if (distance < factor): # 0.05
            return False
        else:
            return True

    # Checking the Orientation between tip and target
    # The smaller value represent to closer with each other
    def checkOrientation (self,factor):
        clientID = self.clientID
        targetHandle = self.targetHandle
        tipHandle = self.tipHandle
        global countOri
        returnCode1 = 1
        returnCode2 = 1
        while(returnCode1==1 and returnCode2==1):
            returnCode1,targetOrientation = vrep.simxGetObjectOrientation(clientID, targetHandle, -1, vrep.simx_opmode_blocking)
            returnCode2,tipOrientation = vrep.simxGetObjectOrientation(clientID, tipHandle, -1, vrep.simx_opmode_blocking)
            print(returnCode1)
            print(returnCode2)
            #print(targetPosition[0],tipPosition[0])
            #print(targetPosition[1],tipPosition[1])
            #print(targetPosition[2],tipPosition[2])
            for i in range(3):
                if (targetOrientation[i] < 0):
                    targetOrientation[i] = float(targetOrientation[i]) * -1
                if (tipOrientation[i] < 0):
                    tipOrientation[i] = float(tipOrientation[i]) * -1
            orientation = math.sqrt(pow(abs(targetOrientation[0]-tipOrientation[0]),2)+pow(abs(targetOrientation[1]-tipOrientation[1]),2)+pow(abs(targetOrientation[2]-tipOrientation[2]),2))
        print(orientation)
        time.sleep(0.1)
        #print(type(orientation))
        if (orientation < factor): #0.07
            return False
        else:
            return True
    
    def checking(self,factor1,factor2):
        count = 0
        while(self.checkDistance(factor1)):
            while(self.checkOrientation(factor2)):
                count += 1

'''
#testing
if __name__ == '__main__':
    test = Check()
    test.checkDistance(0.7)   
    test.checkOrientation(0.7) 
'''