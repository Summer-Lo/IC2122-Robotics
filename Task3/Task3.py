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
import threading


class UR3_RG2:
    # variates
    resolutionX = 640               # Camera resolution: 640*480
    resolutionY = 900
    joint_angle = [0,0,0,0,0,0]     # each angle of joint
    RAD2DEG = 180 / math.pi         # transform radian to degrees
    posOnPath=0
    v = 0.3                         # velocity


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

    def task3c(self):
        movement = Movement.Move()
        information = Information.data()
        checking = Checking.Check()
        print("Process threading now!")
        movement.setTargetPosition_withoutInput(-0.2,0,1.1)
        checking.checking(0.07,0.6)
        movement.setTargetPosition_withoutInput(-0.15,0,1.1)
        checking.checking(0.07,0.08)
        # ----------Write your code here <START>----------
                        
                        
        # ----------Write your code here <END>----------

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
        targetHandle = self.targetHandle
        pos = [-3.8843e-01,-9.8524e-04,+1.1037e+00]
        ori = [0.0058625609574,-0.0041306707407,0.00022043508453]
        vrep.simxSetObjectPosition(clientID, targetHandle, -1, pos, vrep.simx_opmode_blocking)
        vrep.simxSetObjectOrientation(clientID, targetHandle, -1, ori, vrep.simx_opmode_blocking)



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
    manager = pygame_gui.UIManager((800, 930))
    # Introd
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 25), (195, 45)),text='Adjusting Joint Angle',manager=manager)
    button
    #Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 25), (45, 45)),text='+5',manager=manager)
    #Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 25), (45, 45)),text='-5',manager=manager)
    #Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 25), (45, 45)),text='+1',manager=manager)
    #Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 25), (45, 45)),text='-1',manager=manager)
    Status_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 25), (150, 45)),text='Disabled',manager=manager)    
    reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((475, 25), (100, 45)),text='Reset',manager=manager)
    # Joint 1 button
    joint1Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 75), (45, 45)),text='>>',manager=manager)
    joint1Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 75), (45, 45)),text='<<',manager=manager)
    joint1Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 75), (45, 45)),text='>',manager=manager)
    joint1Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 75), (45, 45)),text='<',manager=manager)
    # Joint 2 button
    joint2Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 125), (45, 45)),text='>>',manager=manager)
    joint2Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 125), (45, 45)),text='<<',manager=manager)
    joint2Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 125), (45, 45)),text='>',manager=manager)
    joint2Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 125), (45, 45)),text='<',manager=manager)
    # Joint 3 button
    joint3Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 175), (45, 45)),text='>>',manager=manager)
    joint3Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 175), (45, 45)),text='<<',manager=manager)
    joint3Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 175), (45, 45)),text='>',manager=manager)
    joint3Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 175), (45, 45)),text='<',manager=manager)
    # Joint 4 button
    joint4Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 225), (45, 45)),text='>>',manager=manager)
    joint4Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 225), (45, 45)),text='<<',manager=manager)
    joint4Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 225), (45, 45)),text='>',manager=manager)
    joint4Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 225), (45, 45)),text='<',manager=manager)
    # Joint 5 button
    joint5Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 275), (45, 45)),text='>>',manager=manager)
    joint5Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (45, 45)),text='<<',manager=manager)
    joint5Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (45, 45)),text='>',manager=manager)
    joint5Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 275), (45, 45)),text='<',manager=manager)
    # Joint 6 Button
    joint6Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 325), (45, 45)),text='>>',manager=manager)
    joint6Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 325), (45, 45)),text='<<',manager=manager)
    joint6Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 325), (45, 45)),text='>',manager=manager)
    joint6Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 325), (45, 45)),text='<',manager=manager)
    # Pose
    returnPose_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((65, 375), (160, 45)),text='Home Position (L)',manager=manager)
    openRG2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 375), (150, 45)),text='Open RG2 (Y)',manager=manager)
    closeRG2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((425, 375), (150, 45)),text='Close RG2 (T)',manager=manager) 
    # Set Position and Orientaiton
    setTarget_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((75, 575), (150, 45)),text='Set Target (I)',manager=manager) 
    setPosition_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 575), (160, 45)),text='Set Position (P)',manager=manager) 
    setOrientation_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((430, 575), (180, 45)),text='Set Orientation (O)',manager=manager)
    '''
    # Step for pick and place
    step1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 675), (60, 45)),text='Step1',manager=manager)
    step2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 675), (60, 45)),text='Step2',manager=manager)
    step3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240, 675), (60, 45)),text='Step3',manager=manager)
    step4_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((340, 675), (60, 45)),text='Step4',manager=manager)
    step5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((440, 675), (60, 45)),text='Step5',manager=manager)
    step6_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 675), (60, 45)),text='Step6',manager=manager)
    step7_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 725), (60, 45)),text='Step7',manager=manager)
    step8_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 725), (60, 45)),text='Step8',manager=manager)
    step9_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240, 725), (60, 45)),text='Step9',manager=manager)
    step10_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((340, 725), (60, 45)),text='Step10',manager=manager)
    step11_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((440, 725), (60, 45)),text='Step11',manager=manager)
    step12_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 725), (60, 45)),text='Step12',manager=manager) 
    '''
    # One Step for completing whole task
    complete_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 675), (540, 45)),text='Clicking this button for completing whole task automatically',manager=manager)

    clock = pygame.time.Clock()
    is_running = True



    robot.closeRG2()

    time.sleep(1)

    robot.openRG2()

    time.sleep(1)

    robot.closeRG2()

    time.sleep(1)

    robot.openRG2()

    clock = pygame.time.Clock()

    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(315,842,150,32)
    color_active = pygame.Color('seagreen1')
    color_passive = pygame.Color('white')
    color = color_passive

    active = False
    
    while True:
        # screen.fill((255,255,255))
        time_delta = clock.tick(60)/1000.0
        jointAngle = [0,0,0,0,0,0]
        jointAngle = information.getJointPositionDegree()
        targetinfo = information.getTipInfomation()
        pygame.display.update()
        font = pygame.font.Font('freesansbold.ttf', 20)
        X = 500
        Y = 100
        jointTitle = ['Base (Joint1)','Shoulder (Joint2)','Elbow (Joint3)','Wrist 1 (Joint4)','Wrist 2 (Joint5)','Wrist 3 (Joint6)']
        infoTitle = ['X:','Y:','Z:','Alpha: ','Beta: ','Gamma: ']
        #pygame.draw.rect(screen, white, pygame.Rect(475,75,525,425))
        pygame.display.flip()
        for i in range(6):
            textClear = font.render('              ', True, black, white)
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
            textRectClear.center = (X, Y + (i * 50))
            textRect.center = (X, Y + (i * 50))
            textRectTitle.center = (X-375, Y + (i * 50))
            textRectDegree.center = (X+75, Y + (i * 50))
            screen.blit(textClear, textRectClear)
            screen.blit(text, textRect)
            screen.blit(textTitle, textRectTitle)
            screen.blit(textDegree, textRectDegree)
            # Target Information Title
            textInfoTopic = font.render('------End-Effector (Tip) Position and Orientation------', True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (310, 450 )
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
        
        font = pygame.font.Font('freesansbold.ttf', 15)
        '''
        textStep = font.render('-------Modifying the program for completing this task by clicking buttons--------', True, blue, white)
        textRectStep = textInfoTopic.get_rect()
        textRectStep.center = (300, 650 )
        screen.blit(textStep, textRectStep)
        '''

        textStep = font.render('-------Modifying the program for completing this task by clicking one button--------', True, blue, white)
        textRectStep = textInfoTopic.get_rect()
        textRectStep.center = (280, 650 )
        screen.blit(textStep, textRectStep)
            
            
        pygame.display.update()
        pygame.display.flip()

        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            # exit the program
            if event.type == pygame.QUIT:
                sys.exit()
            # click button
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == reset_button:
                        print('Reset')
                        movement.setObjectInfo(int(hc.obstacleHandle),float(hc.obsposX[0]),float(hc.obsposY[0]),float(hc.obsposZ[0]),float(hc.obsposA[0]),float(hc.obsposB[0]),float(hc.obsposG[0]))
                        movement.setObjectInfo(int(hc.obstacle0Handle),float(hc.obsposX[1]),float(hc.obsposY[1]),float(hc.obsposZ[1]),float(hc.obsposA[1]),float(hc.obsposB[1]),float(hc.obsposG[1]))
                        movement.setObjectInfo(int(hc.obstacle1Handle),float(hc.obsposX[2]),float(hc.obsposY[2]),float(hc.obsposZ[2]),float(hc.obsposA[2]),float(hc.obsposB[2]),float(hc.obsposG[2]))
                        movement.setObjectInfo(int(hc.blueBlockHandle),float(hc.posX[0]),float(hc.posY[0]),float(hc.posZ[0]),float(hc.oriA[0]),float(hc.oriB[0]),float(hc.oriG[0]))
                        movement.setObjectInfo(int(hc.greenBlockHandle),float(hc.posX[1]),float(hc.posY[1]),float(hc.posZ[1]),float(hc.oriA[1]),float(hc.oriB[1]),float(hc.oriG[1]))
                        movement.setObjectInfo(int(hc.greenLakeBlockHandle),float(hc.posX[2]),float(hc.posY[2]),float(hc.posZ[2]),float(hc.oriA[2]),float(hc.oriB[2]),float(hc.oriG[2]))
                        movement.setObjectInfo(int(hc.purpleBlockHandle),float(hc.posX[3]),float(hc.posY[3]),float(hc.posZ[3]),float(hc.oriA[3]),float(hc.oriB[3]),float(hc.oriG[3]))
                        movement.setObjectInfo(int(hc.redBlockHandle),float(hc.posX[4]),float(hc.posY[4]),float(hc.posZ[4]),float(hc.oriA[4]),float(hc.oriB[4]),float(hc.oriG[4]))
                        movement.setObjectInfo(int(hc.whiteBlockHandle),float(hc.posX[5]),float(hc.posY[5]),float(hc.posZ[5]),float(hc.oriA[5]),float(hc.oriB[5]),float(hc.oriG[5]))
                        movement.setObjectInfo(int(hc.yellowBlockHandle),float(hc.posX[6]),float(hc.posY[6]),float(hc.posZ[6]),float(hc.oriA[6]),float(hc.oriB[6]),float(hc.oriG[6]))
                        robot.returnPose()
            if event.type == pygame.USEREVENT:
                # Joint 1
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Add5_button:
                        robot.rotateCertainAnglePositive(0,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Sub5_button:
                        robot.rotateCertainAngleNegative(0,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Add_button:
                        robot.rotateCertainAnglePositive(0,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Sub_button:
                        robot.rotateCertainAngleNegative(0,1)
                # Joint 2
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Add5_button:
                        robot.rotateCertainAnglePositive(1,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Sub5_button:
                        robot.rotateCertainAngleNegative(1,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Add_button:
                        robot.rotateCertainAnglePositive(1,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Sub_button:
                        robot.rotateCertainAngleNegative(1,1)
                # Joint 3
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Add5_button:
                        robot.rotateCertainAnglePositive(2,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Sub5_button:
                        robot.rotateCertainAngleNegative(2,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Add_button:
                        robot.rotateCertainAnglePositive(2,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Sub_button:
                        robot.rotateCertainAngleNegative(2,1)
                # Joint 4
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Add5_button:
                        robot.rotateCertainAnglePositive(3,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Sub5_button:
                        robot.rotateCertainAngleNegative(3,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Add_button:
                        robot.rotateCertainAnglePositive(3,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Sub_button:
                        robot.rotateCertainAngleNegative(3,1)
                # Joint 5
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Add5_button:
                        robot.rotateCertainAnglePositive(4,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Sub5_button:
                        robot.rotateCertainAngleNegative(4,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Add_button:
                        robot.rotateCertainAnglePositive(4,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Sub_button:
                        robot.rotateCertainAngleNegative(4,1)
                # Joint 6
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Add5_button:
                        robot.rotateCertainAnglePositive(5,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Sub5_button:
                        robot.rotateCertainAngleNegative(5,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Add_button:
                        robot.rotateCertainAnglePositive(5,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Sub_button:
                        robot.rotateCertainAngleNegative(5,1)
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

                # Target Position and Orientation
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setTarget_button:
                        if(1 in hc.functionStatus):
                            pass
                        else:
                            active = True 
                            hc.functionStatus[2] = 1    
                            hc.question = hc.setTargetQuestion[0]   
                            hc.inputHeading = "Input: "
                            hc.setTargetStatus[0] = 1
                            print("Set Target Button is clicked!")
                            print("Current function status is: ", hc.functionStatus)
                            print("Current Set Target Status is: ",hc.setTargetStatus)                        
                        #movement.setTarget()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setPosition_button:
                        if(1 in hc.functionStatus):
                            pass
                        else:                        
                            active = True 
                            hc.functionStatus[0] = 1    
                            hc.question = hc.setPosQuestion[0]   
                            hc.inputHeading = "Input: "
                            hc.setPosStatus[0] = 1
                            print("Set Target Button is clicked!")
                            print("Current function status is: ", hc.functionStatus)
                            print("Current Set Position Status is: ",hc.setPosStatus)                         
                        #movement.setTargetPosition()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setOrientation_button:
                        if(1 in hc.functionStatus):
                            pass
                        else:      
                            active = True 
                            hc.functionStatus[1] = 1    
                            hc.question = hc.setOriQuestion[0]  
                            hc.inputHeading = "Input: "
                            hc.setOriStatus[0] = 1
                            print("Set Target Button is clicked!")
                            print("Current function status is: ", hc.functionStatus)
                            print("Current Set Orientation Status is: ",hc.setOriStatus)                         
                        #movement.setTargetOrientation()



                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == complete_button:
                        # Please input your command (functions can be found at Task3.py, Movement.py, Information.py )
                        print("Working........")
                        taskAuto = threading.Thread(target=robot.task3c)
                        taskAuto.start()

                        
            manager.process_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
    
                # Unicode standard is used for string
                # formation
                if event.key == pygame.K_RETURN:
                    # get and print the user inputed message.
                    questionTopicInfo = base_font.render("                                                                                                                           ", True, black, white)
                    questionTopic = pygame.Rect(25,800,700,32)
                    screen.blit(questionTopicInfo, questionTopic)
                    try:
                        userInputCheck = float(user_text)
                        if(user_text != ""):
                            print("The user input: ", user_text[:])
                            hc.userInput = user_text[:]
                            print("The value passed to the function")
                            for i in range(len(hc.functionStatus)):
                                if(hc.functionStatus[i] == 1):                                          # hc.functionStatus[] = ["SetPos","SetOri","SetTarget"]
                                    print("Working with function ", int(i))

                                    if(int(i) == 0):							# Checking whether function1 (setTarget) is using
                                        #print(int(i) == 0)
                                        print("1 in hc.setPosStatus? ",1 in hc.setPosStatus)
                                        if(1 in hc.setPosStatus):
                                            j = int(hc.setPosStatus.index(1))
                                            print("Current J used is: ", int(j))
                                            hc.setPosValue[j] = float(user_text)
                                            hc.setPosStatus[j] = 0
                                            user_text = ""
                                            print("Current Set Position Status is: ",hc.setPosStatus)
                                            if (j <=1):
                                                hc.question = "                                                                                                                          "
                                                print(" j <= 1")
                                                hc.setPosStatus[int(j)+1] = 1
                                                hc.question = hc.setPosQuestion[int(j)+1]
                                            if (j == 2):
                                                hc.question = ""
                                                movement.setTargetPosition()
                                                hc.functionStatus[i] = 0
                                                active = False
                                                print("Status: ",hc.functionStatus)
                                                #hc.question = "-------------------------------------------------------------------------------------"
                                                hc.question = "                                                                                                          "
                                                hc.inputHeading = "                         "

                                    if(int(i) == 1):							# Checking whether function1 (setTarget) is using
                                        #print(int(i) == 0)
                                        print("1 in hc.setOriStatus? ",1 in hc.setOriStatus)
                                        if(1 in hc.setOriStatus):
                                            j = int(hc.setOriStatus.index(1))
                                            print("Current J used is: ", int(j))
                                            hc.setOriValue[j] = float(user_text)
                                            hc.setOriStatus[j] = 0
                                            user_text = ""
                                            print("Current Set Orientation Status is: ",hc.setTargetStatus)
                                            if (j <=1):
                                                hc.question = "                                                                                                                          "
                                                print(" j <= 1")
                                                hc.setOriStatus[int(j)+1] = 1
                                                hc.question = hc.setOriQuestion[int(j)+1]
                                            if (j == 2):
                                                hc.question = ""
                                                movement.setTargetOrientation()
                                                hc.functionStatus[i] = 0
                                                active = False
                                                print("Status: ",hc.functionStatus)
                                                #hc.question = "-------------------------------------------------------------------------------------"
                                                hc.question = "                                                                                                          "
                                                hc.inputHeading = "                         "

                                    elif(int(i) == 2):							# Checking whether function1 (setTarget) is using
                                        #print(int(i) == 0)
                                        print("1 in hc.setTargetStatus? ",1 in hc.setTargetStatus)
                                        if(1 in hc.setTargetStatus):
                                            j = int(hc.setTargetStatus.index(1))
                                            print("Current J used is: ", int(j))
                                            hc.setTargetValue[j] = float(user_text)
                                            hc.setTargetStatus[j] = 0
                                            user_text = ""
                                            print("Current Set Target Status is: ",hc.setTargetStatus)
                                            if (j <=4):
                                                hc.question = "                                                                                                                          "
                                                print(" j <= 4")
                                                hc.setTargetStatus[int(j)+1] = 1
                                                hc.question = hc.setTargetQuestion[int(j)+1]
                                            if (j == 5):
                                                hc.question = ""
                                                movement.setTarget()
                                                hc.functionStatus[i] = 0
                                                active = False
                                                print("Status: ",hc.functionStatus)
                                                #hc.question = "-------------------------------------------------------------------------------------"
                                                hc.question = "                                                                                                          "
                                                hc.inputHeading = "                         "
                                    # Reset the user input after function executed
                                    print(hc.functionStatus)
                                    user_text = ""
                                    hc.userInput = user_text

                    except:
                        user_text = "Error"
                else:
                    if(active == True):
                        if(event.unicode != "\b" and event.unicode != "\r"):
                            user_text += event.unicode

        questionTopicInfo = base_font.render("------------------- User Input -------------------", True, blue, white)
        questionTopic = pygame.Rect(115,750,700,32)
        screen.blit(questionTopicInfo, questionTopic)

        questionTopicInfo = base_font.render(hc.question, True, black, white)
        questionTopic = pygame.Rect(25,800,700,32)
        screen.blit(questionTopicInfo, questionTopic)

        inputTopicInfo = base_font.render(hc.inputHeading, True, blue, white)
        inputTopic = pygame.Rect(240,850,50,32)
        screen.blit(inputTopicInfo, inputTopic)

        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect)
  
        text_surface = base_font.render(user_text, True, (0,0,0))
        
        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        
        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)

        clock.tick(60)
        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()
                    
if __name__ == '__main__':
    main()

