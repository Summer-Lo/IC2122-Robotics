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

    # Rotate the ?th joint with ? angle (clockwise)
    # num should be input the order of joint (e.g.: if you selected joint1, num should be 0)
    def rotateCertainAnglePositive(self, num, angle):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        jointConfig = self.jointConfig
        jointNum = self.jointNum
        
        vrep.simxSetJointTargetPosition(clientID, jointHandle[num], (jointConfig[num]+angle)/RAD2DEG, vrep.simx_opmode_oneshot)     # Set the specific joint angle
        jointConfig[num] = jointConfig[num] + angle
        
        self.jointConfig = jointConfig
        
    # Rotate the ?th joint with ? angle (anti-clockwise)
    # num should be input the order of joint (e.g.: if you selected joint1, num should be 0)
    def rotateCertainAngleNegative(self, num, angle):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        jointConfig = self.jointConfig
        
        vrep.simxSetJointTargetPosition(clientID, jointHandle[num], (jointConfig[num]-angle)/RAD2DEG, vrep.simx_opmode_oneshot)     # Set the specific joint angle
        jointConfig[num] = jointConfig[num] - angle
        
        self.jointConfig = jointConfig

    # Set the joint angle by user input
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
        for i in range(6):                                                                                                          # loop 6 times for setting 6 joint angle
            vrep.simxSetJointTargetPosition(clientID, jointHandle[i], jointAngle[i]/RAD2DEG, vrep.simx_opmode_oneshot)              # Set the specific joint angle
        self.jointConfig = jointConfig

    # Set the target position and orientaion
    # target position and orientation will affect the position and orientaion of end-effector
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
        vrep.simxSetObjectPosition(clientID, targetHandle, -1, position, vrep.simx_opmode_blocking)                                 # Set the target position
        vrep.simxSetObjectOrientation(clientID, targetHandle, -1, orientation, vrep.simx_opmode_blocking)                           # Set the target orientation

    # Set the target position
    # target position will affect the end-effector's position 
    def setTargetPosition(self):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        targetHandle = self.targetHandle
        PosX = float(input("Input Position X: "))
        PosY = float(input("Input Position Y: "))
        PosZ = float(input("Input Position Z: "))
        position = [float(PosX),float(PosY),float(PosZ)]
        vrep.simxSetObjectPosition(clientID, targetHandle, -1, position, vrep.simx_opmode_blocking)                                 # Set the target position
        
    # Set the target orientation
    # target orientation will affect the end-effector's orientation 
    def setTargetOrientation(self):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        targetHandle = self.targetHandle
        Alpha = float(input("Input Orientation Alpha (in degree): "))/RAD2DEG
        Beta = float(input("Input Orientation Beta (in degree): "))/RAD2DEG
        Gamma = float(input("Input Orientation Gamma (in degree): "))/RAD2DEG
        orientation = [float(Alpha),float(Beta),float(Gamma)]
        vrep.simxSetObjectOrientation(clientID, targetHandle, -1, orientation, vrep.simx_opmode_blocking)                           # Set the target orientation

    # Set the target position and orientaion without user input at administrator
    # target position and orientation (degree) will affect the position and orientaion of end-effector
    def setTarget_withoutInput(self,PosX,PosY,PosZ,Alpha,Beta,Gamma):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        targetHandle = self.targetHandle
        position = [float(PosX),float(PosY),float(PosZ)]
        orientation = [float(Alpha)/RAD2DEG,float(Beta)/RAD2DEG,float(Gamma)/RAD2DEG]
        vrep.simxSetObjectPosition(clientID, targetHandle, -1, position, vrep.simx_opmode_blocking)                                 # Set the target position
        vrep.simxSetObjectOrientation(clientID, targetHandle, -1, orientation, vrep.simx_opmode_blocking)                           # Set the target orientation

    # Set the target position without user input at administrator
    # target position will affect the end-effector's position 
    def setTargetPosition_withoutInput(self,PosX,PosY,PosZ):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        targetHandle = self.targetHandle
        position = [float(PosX),float(PosY),float(PosZ)]
        vrep.simxSetObjectPosition(clientID, targetHandle, -1, position, vrep.simx_opmode_blocking)                                 # Set the target position
        
    # Set the target orientation without user input at administrator
    # target orientation (degree) will affect the end-effector's orientation 
    def setTargetOrientation_withoutInput(self,Alpha,Beta,Gamma):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        targetHandle = self.targetHandle
        orientation = [float(Alpha)/RAD2DEG,float(Beta)/RAD2DEG,float(Gamma)/RAD2DEG]
        vrep.simxSetObjectOrientation(clientID, targetHandle, -1, orientation, vrep.simx_opmode_blocking)                           # Set the target orientation

'''
#testing
if __name__ == '__main__':
    test = Move()
    test.setTargetPosition()
    #main()
'''
    
    