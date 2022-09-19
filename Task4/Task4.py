#-*- coding:utf-8 -*-

"""
keyboard Instructions:
    robot moving velocity: <=5(advise)
    Q,W: joint 0
    A,S: joint 1
    Z,X: joint 2
    E,R: joint 3
    D,F: joint 4
    C,V: joint 5
    P: exit()
    T: close RG2
    Y: open RG2
"""

import sys
import math
import time
import pygame
import pygame_gui
import numpy as np
import Information
import Movement
import Checking
import client_config as hc
import vrep
import os

class UR3_RG2:
    # variates
    resolutionX = 740               # Camera resolution: 640*480
    resolutionY = 625
    joint_angle = [0,0,0,0,0,0]     # each angle of joint
    RAD2DEG = 180 / math.pi         # transform radian to degrees
    posOnPath=0
    v = 0.3                         # velocity

    # Handles information
    #jointNum = 6
    #baseName = 'UR3'
    #rgName = 'RG2'
    #jointName = 'UR3_joint'
    #camera_rgb_Name = 'kinect_rgb'
    #camera_depth_Name = 'kinect_depth'
    #tipName = 'tip'
    #targetName = 'target'
    #pathName = 'Path'
    #visionSensorName = 'Vision_sensor'
    #camName = 'cam'

    # communication and read the handles
    def __init__(self):
        self.jointNum = hc.jointNum
        self.baseName = hc.baseName
        self.rgName = hc.rgName
        self.jointName = hc.jointName
        self.camera_rgb_Name = hc.camera_rgb_Name
        self.camera_depth_Name = hc.camera_depth_Name
        self.tipName = hc.tipName
        self.targetName = hc.targetName
        self.pathName = hc.pathName
        self.visionSensorName = hc.visionSensorName
        self.camName = hc.camName
             
        self.clientID = hc.clientID
        self.jointHandle = hc.jointHandle
        self.baseHandle = hc.baseHandle
        self.rgHandle = hc.rgHandle
        self.cameraRGBHandle = hc.cameraRGBHandle
        self.cameraDepthHandle = hc.cameraDepthHandle
        self.jointConfig = hc.jointConfig
        self.tipHandle = hc.tipHandle
        self.targetHandle = hc.targetHandle
        self.pathHandle = hc.pathHandle
        self.visionSensorHandle = hc.visionSensorHandle
        self.camHandle = hc.camHandle
        # UR3 (Right)
        self.rgName0 = hc.rgName0
        # UR3 (Right)
        self.jointHandle0 = hc.jointHandle0
        self.baseHandle0 = hc.baseHandle0
        self.rgHandle0 = hc.rgHandle0
        self.jointConfig0 = hc.jointConfig0
        self.tipHandle0 = hc.tipHandle0
        self.targetHandle0 = hc.targetHandle0

    # disconnect
    def __del__(self):
        clientID = self.clientID
        vrep.simxFinish(clientID)
        print('Simulation end')
        
    # show Handles information
    def showHandles(self):
        
        RAD2DEG = self.RAD2DEG
        jointNum = self.jointNum
        clientID = self.clientID
        jointHandle = self.jointHandle
        rgHandle = self.rgHandle
        cameraRGBHandle = self.cameraRGBHandle
        cameraDepthHandle = self.cameraDepthHandle
        
        print('Handles available!')
        print("==============================================")
        print("Handles:  ")
        for i in range(len(jointHandle)):
            print("jointHandle" + str(i+1) + ": " + jointHandle[i])
        print("rgHandle:" + rgHandle)
        print("cameraRGBHandle:" + cameraRGBHandle)
        print("cameraDepthHandle:" + cameraDepthHandle)
        print("===============================================")
        
    # show each joint's angle
    def showJointAngles(self):
        RAD2DEG = self.RAD2DEG
        jointNum = self.jointNum
        clientID = self.clientID
        jointHandle = self.jointHandle
        
        for i in range(jointNum):
            _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_blocking)
            print(round(float(jpos) * RAD2DEG, 2))
        print('\n')

    # open rg2
    def openRG2(self):
        rgName = self.rgName
        clientID = self.clientID
        res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, rgName,\
                                                        vrep.sim_scripttype_childscript,'rg2Open',[],[],[],b'',vrep.simx_opmode_blocking)
        
    # close rg2
    def closeRG2(self):
        rgName = self.rgName
        clientID = self.clientID
        res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, rgName,\
                                                        vrep.sim_scripttype_childscript,'rg2Close',[],[],[],b'',vrep.simx_opmode_blocking)
    
    def openRG20(self):
        rgName0 = self.rgName0
        clientID = self.clientID
        res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, rgName0,\
                                                        vrep.sim_scripttype_childscript,'rg2Open',[],[],[],b'',vrep.simx_opmode_blocking)
        
    # close rg2
    def closeRG20(self):
        rgName0 = self.rgName0
        clientID = self.clientID
        res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, rgName0,\
                                                        vrep.sim_scripttype_childscript,'rg2Close',[],[],[],b'',vrep.simx_opmode_blocking)
        

    def StopSimulation(self):
        clientID = self.clientID
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)    # Stop simulation
        vrep.simxFinish(clientID)   # Finish
    
    
    # Rotate the ?th joint with ? angle (clockwise)
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
    # Return to the original pose for further testing
    def returnPose(self):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        jointConfig = hc.jointConfig
        for i in range(6):
            vrep.simxSetJointTargetPosition(clientID, jointHandle[i], 0, vrep.simx_opmode_oneshot)
            jointConfig[i] = 0
        hc.jointConfig = jointConfig
        #targetHandle = self.targetHandle
        #pos = [-4.7965e-03,3.8874e-01,1.1039e+00]
        #ori = [2.8907888401,-1.5369718459,1.4156714629]
        #vrep.simxSetObjectPosition(clientID, targetHandle, -1, pos, vrep.simx_opmode_blocking)
        #vrep.simxSetObjectOrientation(clientID, targetHandle, -1, ori, vrep.simx_opmode_blocking)

    def returnPose0(self):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        #targetHandle0 = self.targetHandle0
        jointHandle0 = self.jointHandle0
        jointConfig0 = hc.jointConfig0
        for i in range(6):
            vrep.simxSetJointTargetPosition(clientID, jointHandle0[i], 0, vrep.simx_opmode_oneshot)
            jointConfig0[i] = 0
        hc.jointConfig0 = jointConfig0
        #pos = [6.9520e-01,3.8874e-01,1.1039e+00]
        #ori = [2.8714156854,-1.5384902823,1.3964030279]
        #vrep.simxSetObjectPosition(clientID, targetHandle0, -1, pos, vrep.simx_opmode_blocking)
        #vrep.simxSetObjectOrientation(clientID, targetHandle0, -1, ori, vrep.simx_opmode_blocking)



# control robot by keyboard
def main():
    robot = UR3_RG2()
    resolutionX = robot.resolutionX
    resolutionY = robot.resolutionY
    movement = Movement.Move()
    information = Information.data()
    checking = Checking.Check()
    
    #angle = float(eval(input("please input velocity: ")))
    angle = 1
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (68,28)
    pygame.init()
    screen = pygame.display.set_mode((resolutionX, resolutionY))
    screen.fill((255,255,255))
    pygame.display.set_caption("VREP Control Panel")
    # looping, can resume moving with pressing one key
    pygame.key.set_repeat(200,50)
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    black = (0, 0, 0)
    manager = pygame_gui.UIManager((800, 880))
    # Introd
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 25), (185, 45)),text='UR3 (Left)',manager=manager)
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((470, 25), (185, 45)),text='UR3 (Right)',manager=manager)

    # Pose
    returnPose_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 375), (115, 45)),text='Home Position',manager=manager)
    openRG2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((135, 375), (100, 45)),text='Open RG2',manager=manager)
    closeRG2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((245, 375), (100, 45)),text='Close RG2',manager=manager) 
    returnPose0_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((380, 375), (115, 45)),text='Home Position',manager=manager)
    openRG20_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((505, 375), (100, 45)),text='Open RG2',manager=manager)
    closeRG20_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((615, 375), (100, 45)),text='Close RG2',manager=manager) 
    # Set Position and Orientaiton
    setTarget_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 575), (150, 45)),text='Set Target',manager=manager) 
    setPosition_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 575), (150, 45)),text='Set Position',manager=manager) 
    setOrientation_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 575), (150, 45)),text='Set Orientation',manager=manager)
    '''
    setTarget0_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 775), (150, 45)),text='Set Target',manager=manager) 
    setPosition0_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 775), (150, 45)),text='Set Position',manager=manager) 
    setOrientation0_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 775), (150, 45)),text='Set Orientation',manager=manager)
    '''
    '''
    # Calucation Pose
    pose1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 625), (150, 45)),text='Pose 1',manager=manager)
    pose2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 625), (150, 45)),text='Pose 2',manager=manager)
    pose3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 625), (150, 45)),text='Pose 3',manager=manager)
    '''
    clock = pygame.time.Clock()
    is_running = True



    robot.closeRG2()

    time.sleep(1)

    robot.openRG2()

    time.sleep(1)

    robot.closeRG2()

    time.sleep(1)

    robot.openRG2()
    
    while True:
        # screen.fill((255,255,255))
        #ur30_angle = information.getJointPositionRadius()
        time_delta = clock.tick(60)/1000.0
        jointAngle = [0,0,0,0,0,0]
        jointAngle = information.getJointPositionDegree()
        targetinfo = information.getTargetInfomation()
        jointAngle0 = information.getJoint0PositionDegree()
        targetinfo0 = information.getTarget0Infomation()
        pygame.display.update()
        font = pygame.font.Font('freesansbold.ttf', 20)
        X = 500
        Y = 100
        jointTitle = ['Base (Joint1)','Shoulder (Joint2)','Elbow (Joint3)','Wrist 1 (Joint4)','Wrist 2 (Joint5)','Wrist 3 (Joint6)']
        infoTitle = ['X:','Y:','Z:','Alpha: ','Beta: ','Gamma: ']
        #pygame.draw.rect(screen, white, pygame.Rect(475,75,525,425))
        pygame.display.flip()
        for i in range(6):
            textClear = font.render('                     ', True, black, white)
            if (jointAngle[i] >= 0 and jointAngle[i] != -0.0):
                text = font.render('+' + str(jointAngle[i]), True, blue, white)
            else:
                text = font.render(str(jointAngle[i]), True, blue, white)
            textTitle = font.render(str(jointTitle[i]), True, black, white)
            textDegree = font.render('deg', True, black, white)
            textRectClear = textClear.get_rect()
            textRect = text.get_rect()
            textRectTitle = textTitle.get_rect()
            textRectDegree = textDegree.get_rect()
            textRectClear.center = (225, Y + (i * 50))
            textRect.center = (250, Y + (i * 50))
            textRectTitle.center = (X-375, Y + (i * 50))
            textRectDegree.center = (325, Y + (i * 50))
            screen.blit(textClear, textRectClear)
            screen.blit(text, textRect)
            screen.blit(textTitle, textRectTitle)
            screen.blit(textDegree, textRectDegree)
            # Target Information Title
            textInfoTopic = font.render('---UR3 (Left) End-Effector (Tip) Position (Base) and Orientation---', True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (365, 450 )
            screen.blit(textInfoTopic, textRectInfoTopic)
            textInfoTitle = font.render(str(infoTitle[i]), True, black, white)
            textRectInfoTitle = textInfoTitle.get_rect()
            if (i <= 2):
                textRectInfoTitle.center = (X-400 +(i*200), 500 )
            else:
                textRectInfoTitle.center = (X-400 +((i-3)*187), 550 )
            screen.blit(textInfoTitle, textRectInfoTitle)
            
            # Target Information Clear
            textInfoClear = font.render('                 ', True, black, white)
            textRectInfoClear = textInfoClear.get_rect()
            if (i <= 2):
                textRectInfoClear.center = (X-330 +(i*200), 500 )
            elif (i == 3):
                textRectInfoClear.center = (X-320, 550 )
            elif (i == 4):
                textRectInfoClear.center = (X-140, 550 )
            elif (i == 5):
                textRectInfoClear.center = (X+75, 550 )
            screen.blit(textInfoClear, textRectInfoClear)
            
            # Target Information
            if (i <= 2):
                textInfo = font.render(str(targetinfo[i])+' m', True, black, white)
            else:
                textInfo = font.render(str(targetinfo[i]), True, black, white)
            textRectInfo = textInfo.get_rect()
            if (i <= 2):
                textRectInfo.center = (X-330 +(i*200), 500 )
            elif (i == 3):
                textRectInfo.center = (X-320, 550 )
            elif (i == 4):
                textRectInfo.center = (X-140, 550 )
            elif (i == 5):
                textRectInfo.center = (X+75, 550 )
            screen.blit(textInfo, textRectInfo)
        # UR3#0
        
        for i in range(6):
            X = 850
            textClear = font.render('                     ', True, black, white)
            if (jointAngle0[i] >= 0 and jointAngle0[i] != -0.0):
                text = font.render('+' + str(jointAngle0[i]), True, blue, white)
            else:
                text = font.render(str(jointAngle0[i]), True, blue, white)
            textTitle = font.render(str(jointTitle[i]), True, black, white)
            textDegree = font.render('deg', True, black, white)
            textRectClear = textClear.get_rect()
            textRect = text.get_rect()
            textRectTitle = textTitle.get_rect()
            textRectDegree = textDegree.get_rect()
            textRectClear.center = (575, Y + (i * 50))
            textRect.center = (600, Y + (i * 50))
            textRectTitle.center = (X-375, Y + (i * 50))
            textRectDegree.center = (675, Y + (i * 50))
            screen.blit(textClear, textRectClear)
            screen.blit(text, textRect)
            screen.blit(textTitle, textRectTitle)
            screen.blit(textDegree, textRectDegree)
            X = 500
            '''
            # Target Information Title
            textInfoTopic = font.render('---UR3 (Right) End-Effector (Tip) Position (World) and Orientation---', True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (365, 650 )
            screen.blit(textInfoTopic, textRectInfoTopic)
            textInfoTitle = font.render(str(infoTitle[i]), True, black, white)
            textRectInfoTitle = textInfoTitle.get_rect()
            if (i <= 2):
                textRectInfoTitle.center = (X-400 +(i*200), 700 )
            else:
                textRectInfoTitle.center = (X-400 +((i-3)*187), 750 )
            screen.blit(textInfoTitle, textRectInfoTitle)
            
            # Target Information Clear
            textInfoClear = font.render('                 ', True, black, white)
            textRectInfoClear = textInfoClear.get_rect()
            if (i <= 2):
                textRectInfoClear.center = (X-330 +(i*200), 700 )
            elif (i == 3):
                textRectInfoClear.center = (X-320, 750 )
            elif (i == 4):
                textRectInfoClear.center = (X-140, 750 )
            elif (i == 5):
                textRectInfoClear.center = (X+75, 750 )
            screen.blit(textInfoClear, textRectInfoClear)
            
            # Target Information
            if (i <= 2):
                textInfo = font.render(str(targetinfo0[i])+' m', True, black, white)
            else:
                textInfo = font.render(str(targetinfo0[i]), True, black, white)
            textRectInfo = textInfo.get_rect()
            if (i <= 2):
                textRectInfo.center = (X-330 +(i*200), 700 )
            elif (i == 3):
                textRectInfo.center = (X-320, 750 )
            elif (i == 4):
                textRectInfo.center = (X-140, 750 )
            elif (i == 5):
                textRectInfo.center = (X+75, 750 )
            screen.blit(textInfo, textRectInfo)
            '''
            
            
        pygame.display.update()
        pygame.display.flip()

        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            # exit the program
            if event.type == pygame.QUIT:
                sys.exit()
            # click button
            if event.type == pygame.USEREVENT:
                # Joint 1
                # Pose
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == returnPose_button:
                        robot.returnPose()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == openRG2_button:
                        robot.openRG2()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == closeRG2_button:
                        robot.closeRG2()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setTarget_button:
                        movement.setTarget()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setPosition_button:
                        movement.setTargetPosition()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setOrientation_button:
                        movement.setTargetOrientation()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == returnPose0_button:
                        robot.returnPose0()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == openRG20_button:
                        robot.openRG20()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == closeRG20_button:
                        robot.closeRG20()
                '''
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setTarget0_button:
                        movement.setTarget0()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setPosition0_button:
                        movement.setTargetPosition0()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setOrientation0_button:
                        movement.setTargetOrientation0()
                '''
                '''
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == pose1_button:
                        movement.setJointAngle1(-90,0,0,0,0,0)
                        #movement.setJointAngle1(-45.99,-51.94,53.75,-1.54,80.82,3.16)
                        movement.setJointAngle0(90,0,0,0,0,0)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == pose2_button:
                        movement.setTarget_withoutInput(0.35,0.3,0.635,0,90,180)
                        checking.checking(0.07,0.6)
                        time.sleep(2)
                        movement.setTarget_withoutInput(0.35,0.3,0.435,0,90,180)
                        checking.checking(0.07,0.6)
                        time.sleep(2)
                        movement.setTarget_withoutInput(0.35,0.3,0.45,0,90,180)
                        checking.checking(0.07,0.6)
                        time.sleep(1)
                        movement.setTarget_withoutInput(0.35,0.3,0.5,0,90,180)
                        checking.checking(0.07,0.6)
                        time.sleep(1)
                        movement.setTarget_withoutInput(-0.0048116,0.38861,1.1039,172.30,-88.070,80.779)
                        time.sleep(2)
                        movement.setTarget0_withoutInput(0.35,0.3,0.635,0,90,180)
                        time.sleep(10)
                        movement.setTarget0_withoutInput(0.35,0.3,0.435,0,90,180)
                        time.sleep(5)
                        movement.setTarget0_withoutInput(0.31129,0.59525,1.1039,91.822,0.28286,-1.5211)
                        time.sleep(2)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == pose3_button:
                        movement.setTarget_withoutInput(0.2,-0.2,0.6,0,90,180)
                        checking.checking(0.07,0.6)
                        movement.setTarget_withoutInput(0.2,-0.2,0.5,0,90,180)
                        checking.checking(0.07,0.6)
                        movement.setTarget_withoutInput(0.2,-0.2,0.435,0,90,180)
                        checking.checking(0.07,0.6)
                        time.sleep(5)
                        movement.setTarget_withoutInput(0.2,-0.2,0.5,0,90,180)
                        checking.checking(0.07,0.6)
                        time.sleep(4)
                        movement.setTarget_withoutInput(0.28861,0.0048163,1.1040,-91.822,-0.2828,178.48)
                        time.sleep(4)
                        movement.setTarget_withoutInput(0.38861,0.0048163,1.1040,-91.822,-0.2828,178.48)
                        time.sleep(2)
                        movement.setTarget0_withoutInput(0.2,-0.2,0.7,0,90,180)
                        time.sleep(6)
                        movement.setTarget0_withoutInput(0.2,-0.2,0.435,0,90,180)
                        time.sleep(8)
                        movement.setTarget0_withoutInput(0.3952,-0.11264,1.1039,171.18,-88.157,79.66)
                        time.sleep(4)
                        movement.setTarget0_withoutInput(0.3952,-0.01264,1.1039,171.18,-88.157,79.66)
                        time.sleep(2)
                '''
                     

            manager.process_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    robot.StopSimulation()
                    sys.exit()
                # joinit 0
                elif event.key == pygame.K_q:
                    movement.rotateCertainAnglePositive(0, angle)
                elif event.key == pygame.K_w:
                    movement.rotateCertainAngleNegative(0, angle)
                # joinit 1
                elif event.key == pygame.K_a:
                    movement.rotateCertainAnglePositive(1, angle)
                elif event.key == pygame.K_s:
                    movement.rotateCertainAngleNegative(1, angle)
                # joinit 2
                elif event.key == pygame.K_z:
                    movement.rotateCertainAnglePositive(2, angle)
                elif event.key == pygame.K_x:
                    movement.rotateCertainAngleNegative(2, angle)
                # joinit 3
                elif event.key == pygame.K_e:
                    movement.rotateCertainAnglePositive(3, angle)
                elif event.key == pygame.K_r:
                    movement.rotateCertainAngleNegative(3, angle)
                # joinit 4
                elif event.key == pygame.K_d:
                    movement.rotateCertainAnglePositive(4, angle)
                elif event.key == pygame.K_f:
                    movement.rotateCertainAngleNegative(4, angle)
                # joinit 5
                elif event.key == pygame.K_c:
                    movement.rotateCertainAnglePositive(5, angle)
                elif event.key == pygame.K_v:
                    movement.rotateCertainAngleNegative(5, angle)
                # close RG2
                elif event.key == pygame.K_t:
                    robot.closeRG2()
                # # open RG2
                elif event.key == pygame.K_y:
                    robot.openRG2()
                # reset angle
                elif event.key == pygame.K_l:# return to the origin pose
                    robot.returnPose()
                # Set target position and orientation (IK)
                elif event.key == pygame.K_i:
                    movement.setTarget()
                # Set target position to make the end-effector arrive the target
                elif event.key == pygame.K_p:
                    movement.setTargetPosition()
                # Set target orientation to make the end-effector arrive the target  
                elif event.key == pygame.K_o:
                    movement.setTargetOrientation()
                    
                # reset angle
                else:
                    print("Invalid input, no corresponding function for this key!")

        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()
                    
if __name__ == '__main__':
    main()

