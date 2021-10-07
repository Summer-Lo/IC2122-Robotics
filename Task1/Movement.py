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
        jointConfig = hc.jointConfig
        jointNum = self.jointNum
        
        vrep.simxSetJointTargetPosition(clientID, jointHandle[num], (jointConfig[num]+angle)/RAD2DEG, vrep.simx_opmode_oneshot)
        jointConfig[num] = jointConfig[num] + angle
        
        hc.jointConfig = jointConfig
        
    # Rotate the ?th joint with ? angle (anti-clockwise)
    def rotateCertainAngleNegative(self, num, angle):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        jointConfig = hc.jointConfig
        
        vrep.simxSetJointTargetPosition(clientID, jointHandle[num], (jointConfig[num]-angle)/RAD2DEG, vrep.simx_opmode_oneshot)
        jointConfig[num] = jointConfig[num] - angle
        
        hc.jointConfig = jointConfig

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
        # ReturnPose: [-3.8728e-01,-1.8161e-03,1.1] [-1.5952833]
        # Blocks:
        # orientation: [-1.47890474,0.0259879526,-1.57311761]
        # red: [1.2500e-01,-3.5000e-01,4.3600e-01]
        # yellow: [2.5000e-01,-2.2500e-01,4.3600e-01]
        # GreenLake: [3.5000e-01,-1.2500e-01,4.3600e-01]
        # blue: [3.5000e-01,2.5000e-02,4.3600e-01]
        # Green: [2.7500e-01,2.0000e-01,4.3600e-01]
        # white: [1.2500e-01,3.2500e-01,4.3600e-01]
        # purple: [-5.0000e-02,3.5000e-01,4.3600e-01]

    # Setting the joint angle for attach Digital twins
    def setJointAngle(self, angle):
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

#testing
if __name__ == '__main__':
    test = Move()
    
    #test.SetTarget(0.125,-0.35,0.435,-1.47890474,0.0259879526,-1.57311761)
    test.SetTarget(2.5000e-01,-2.2500e-01,4.3500e-01,-1.48408837,0.04002563574,-1.41657903)
    #main()
    