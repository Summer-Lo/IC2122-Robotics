import numpy as np
import math
import time
import client_config as hc
import time
import vrep


class Move:
    RAD2DEG = 180 / math.pi

    def __init__(self):
        self.jointConfig = hc.jointConfig
        self.clientID = hc.clientID
        self.baseHandle = hc.baseHandle
        self.joint6Handle = hc.joint6Handle
        self.jointHandle = hc.jointHandle
        self.jointNum = hc.jointNum
        self.targetHandle = hc.targetHandle

    # joint_angle: return the origin angle of each joint ([0,0,0,0,0,0])
    def rotateAllAngle(self, joint_angle):
        clientID = self.clientID
        jointNum = self.jointNum
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        
        # pause the communication and store the necessary command to send together
        vrep.simxPauseCommunication(clientID, True)# Pause
        for i in range(jointNum):
            vrep.simxSetJointTargetPosition(clientID, jointHandle[i], joint_angle[i]/RAD2DEG, vrep.simx_opmode_oneshot)
        vrep.simxPauseCommunication(clientID, False)# Resume
        
        self.jointConfig = joint_angle

    def rotateCertainAnglePositive(self, num, angle):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        jointConfig = self.jointConfig
        jointNum = self.jointNum
        
        vrep.simxSetJointTargetPosition(clientID, jointHandle[num], (jointConfig[num]+angle)/RAD2DEG, vrep.simx_opmode_oneshot)
        jointConfig[num] = jointConfig[num] + angle
        
        self.jointConfig = jointConfig
        
    # Rotate the ?th joint with ? angle (anti-clockwise)
    def rotateCertainAngleNegative(self, num, angle):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        jointConfig = self.jointConfig
        
        vrep.simxSetJointTargetPosition(clientID, jointHandle[num], (jointConfig[num]-angle)/RAD2DEG, vrep.simx_opmode_oneshot)
        jointConfig[num] = jointConfig[num] - angle
        
        self.jointConfig = jointConfig

    # Set the target position whcih will attract the UR end-effector via IK
    # Beware the collision if there are some objects located at the target position. (Setting way point to avoid it)
    def SetTarget (self,X,Y,Z,Alpha,Beta,Gamma):
        clientID = self.clientID
        targetHandle = self.targetHandle
        returnCode = 1
        returnCode1 = 1
        while(returnCode==1 or returnCode1==1):
            returnCode, targetPosition = vrep.simxGetObjectPosition(clientID, targetHandle, -1, vrep.simx_opmode_oneshot)
            returnCode1, targetOrientation = vrep.simxGetObjectOrientation(clientID, targetHandle, -1, vrep.simx_opmode_oneshot)
            #print(returnCode,returnCode1)
            #print(targetPosition,targetOrientation)
        print("Target current position:", targetPosition)
        print("Target current orientation:", targetOrientation)
        PositionX = float(X)        # Corresponding to the world position system
        PositionY = float(Y)
        PositionZ = float(Z)
        Alpha = float(Alpha)        # Corresponding to the world orientation system
        Beta = float(Beta)
        Gamma = float(Gamma)
        #print("Position X: ",PositionX,"Position Y: ",PositionY,"Position Z: ",PositionZ)
        #print("Orientation Alpha: ",Alpha,"Orientation Beta: ",Beta,"Orientation Gamma: ",Gamma)
        position = [PositionX,PositionY,PositionZ]
        orientation = [Alpha,Beta,Gamma]
        #print(position)
        _ = vrep.simxSetObjectPosition(clientID, targetHandle, -1, position, vrep.simx_opmode_oneshot)            # Setting the target position
        _ = vrep.simxSetObjectOrientation(clientID, targetHandle, -1, orientation, vrep.simx_opmode_oneshot)      # Setting the target orientation
        time.sleep(1)
        returnCode = 1
        returnCode1 = 1
        while(returnCode==1 or returnCode1==1):                                                                 # Checking the function called sucess or not
            returnCode, currentTargetPosition = vrep.simxGetObjectPosition(clientID, targetHandle, -1, vrep.simx_opmode_blocking)
            returnCode1, currentTargetOrientation = vrep.simxGetObjectOrientation(clientID, targetHandle, -1, vrep.simx_opmode_blocking)
            print(returnCode,returnCode1)
        print("Current position is: ",currentTargetPosition)
        print("Current orientation is: ",currentTargetOrientation)


    # Setting the joint angle for attach Digital twins
    def setURJointAngle(self, angle):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        jointConfig = self.jointConfig
        returnCode = 1
        for i in range(6):                      # Joint angle preparing
            print("Processing joint ",i)
            returnCode = 1
            if(i==1):
                angle[1] = float(angle[1])+90   # Joint2 angle: ur value + 90 = vrep anlge
            if(i==3):
                angle[3] = float(angle[3])+90   # Joint4 angle: ur value + 90 = vrep anlge
            while(returnCode==1):
                returnCode = vrep.simxSetJointTargetPosition(clientID, jointHandle[i], (angle[i])/RAD2DEG, vrep.simx_opmode_blocking)
                print(returnCode)

    def setJointAngle(self):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        jointConfig = self.jointConfig
        joint1 = int(input("Input Joint 1 Angle: "))
        joint2 = int(input("Input Joint 2 Angle: "))
        joint3 = int(input("Input Joint 3 Angle: "))
        joint4 = int(input("Input Joint 4 Angle: "))
        joint5 = int(input("Input Joint 5 Angle: "))
        joint6 = int(input("Input Joint 6 Angle: "))
        jointAngle = [joint1,joint2,joint3,joint4,joint5,joint6]
        for i in range(6):
            vrep.simxSetJointTargetPosition(clientID, jointHandle[i], jointAngle[i]/RAD2DEG, vrep.simx_opmode_oneshot)
        self.jointConfig = jointConfig

    def setTarget(self):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        targetHandle = self.targetHandle
        PosX = float(input("Input Position X: "))
        PosY = float(input("Input Position Y: "))
        PosZ = float(input("Input Position Z: "))
        Alpha = float(input("Input Orientation Alpha (in degree): "))/RAD2DEG
        Beta = float(input("Input Orientation Beta (in degree): "))/RAD2DEG
        Gamma = float(input("Input Orientation Gamma (in degree): "))/RAD2DEG
        position = [float(PosX),float(PosY),float(PosZ)]
        orientation = [float(Alpha),float(Beta),float(Gamma)]
        vrep.simxSetObjectPosition(clientID, targetHandle, -1, position, vrep.simx_opmode_blocking)
        vrep.simxSetObjectOrientation(clientID, targetHandle, -1, orientation, vrep.simx_opmode_blocking)


    def setTargetPosition(self):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        targetHandle = self.targetHandle
        PosX = float(input("Input Position X: "))
        PosY = float(input("Input Position Y: "))
        PosZ = float(input("Input Position Z: "))
        position = [float(PosX),float(PosY),float(PosZ)]
        vrep.simxSetObjectPosition(clientID, targetHandle, -1, position, vrep.simx_opmode_blocking)
        

    def setTargetOrientation(self):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        targetHandle = self.targetHandle
        Alpha = float(input("Input Orientation Alpha (in degree): "))/RAD2DEG
        Beta = float(input("Input Orientation Beta (in degree): "))/RAD2DEG
        Gamma = float(input("Input Orientation Gamma (in degree): "))/RAD2DEG
        orientation = [float(Alpha),float(Beta),float(Gamma)]
        vrep.simxSetObjectOrientation(clientID, targetHandle, -1, orientation, vrep.simx_opmode_blocking)

'''
#testing
if __name__ == '__main__':
    test = Move()
    test.setTargetPosition()
    #main()
'''
    
    