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
import client_config as hc
import vrep
import os

class UR3_RG2:
    # variates
    resolutionX = 640               # Camera resolution: 640*480
    resolutionY = 780
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
    
    
    # Return to the original pose for further testing
    def returnPose(self):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        jointConfig = hc.jointConfig
        for i in range(6):
            vrep.simxSetJointTargetPosition(clientID, jointHandle[i], 0, vrep.simx_opmode_oneshot)
            jointConfig[i] = 0
        hc.jointConfig = jointConfig

    def setJointAngle(self):
        clientID = self.clientID
        RAD2DEG = self.RAD2DEG
        jointHandle = self.jointHandle
        jointConfig = hc.jointConfig
        '''
        joint1 = float(input("Input Joint 1 Angle: "))
        joint2 = float(input("Input Joint 2 Angle: "))
        joint3 = float(input("Input Joint 3 Angle: "))
        joint4 = float(input("Input Joint 4 Angle: "))
        joint5 = float(input("Input Joint 5 Angle: "))
        joint6 = float(input("Input Joint 6 Angle: "))
        jointConfig = [joint1,joint2,joint3,joint4,joint5,joint6]
        '''
        jointConfig = hc.setTargetValue
        print("Joint Config in Set Joint Angle is: ", hc.setTargetValue)
        for i in range(6):
            vrep.simxSetJointTargetPosition(clientID, jointHandle[i], jointConfig[i]/RAD2DEG, vrep.simx_opmode_oneshot)
        hc.jointConfig = jointConfig




# control robot by keyboard
def main():
    robot = UR3_RG2()
    resolutionX = robot.resolutionX
    resolutionY = robot.resolutionY
    movement = Movement.Move()
    information = Information.data()
    
    #angle = float(eval(input("please input velocity: ")))
    angle = 1
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (68,28)
    pygame.init()
    screen = pygame.display.set_mode((resolutionX, resolutionY))
    screen.fill((255,255,255))
    pygame.display.set_caption("VREP Joint Angle Control Panel")
    # looping, can resume moving with pressing one key
    pygame.key.set_repeat(200,50)
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    black = (0, 0, 0)
    manager = pygame_gui.UIManager((800, 750))
    # Introd
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 25), (195, 45)),text='Adjusting Joint Angle',manager=manager)
    Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 25), (45, 45)),text='+5',manager=manager)
    Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 25), (45, 45)),text='-5',manager=manager)
    Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 25), (45, 45)),text='+1',manager=manager)
    Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 25), (45, 45)),text='-1',manager=manager)
    Reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 25), (80, 45)),text='Reset',manager=manager)
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
    returnPose_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((90, 375), (160, 45)),text='Home Position (L)',manager=manager)
    openRG2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 375), (150, 45)),text='Open RG2 (Y)',manager=manager)
    closeRG2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 375), (150, 45)),text='Close RG2 (T)',manager=manager)
    setTarget_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((60, 425), (520, 45)),text='Joint Angle Configuration (input joint angle at administrator)',manager=manager)
    
    clock = pygame.time.Clock()
    # Configurating RG2
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
    input_rect = pygame.Rect(315,742,150,32)
    color_active = pygame.Color('seagreen1')
    color_passive = pygame.Color('white')
    color = color_passive

    active = False


    while True:
        time_delta = clock.tick(60)/1000.0
        jointAngle = [0,0,0,0,0,0]
        jointAngle = information.getJointPositionDegree()
        targetinfo = information.getTargetInfomation()
        pygame.display.update()
        font = pygame.font.Font('freesansbold.ttf', 20)
        X = 500
        Y = 100
        jointTitle = ['Base (Joint1)','Shoulder (Joint2)','Elbow (Joint3)','Wrist 1 (Joint4)','Wrist 2 (Joint5)','Wrist 3 (Joint6)']
        infoTitle = ['X:','Y:','Z:','Alpha: ','Beta: ','Gamma: ']
        pygame.display.flip()
        for i in range(6):
            X = 500
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
            textInfoTopic = font.render('---End-Effector (Tip) Position and Orientation---', True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (310, 500 )
            screen.blit(textInfoTopic, textRectInfoTopic)
            X = 480
            textInfoTitle = font.render(str(infoTitle[i]), True, black, white)
            textRectInfoTitle = textInfoTitle.get_rect()
            if (i <= 2):
                textRectInfoTitle.center = (X-400 +(i*200), 550 )
            else:
                textRectInfoTitle.center = (X-400 +((i-3)*187), 600 )
            screen.blit(textInfoTitle, textRectInfoTitle)
            
            # Target Information Clear
            textInfoClear = font.render('                 ', True, black, white)
            textRectInfoClear = textInfoClear.get_rect()
            if (i <= 2):
                textRectInfoClear.center = (X-330 +(i*200), 550 )
            elif (i == 3):
                textRectInfoClear.center = (X-320, 600 )
            elif (i == 4):
                textRectInfoClear.center = (X-140, 600 )
            elif (i == 5):
                textRectInfoClear.center = (X+75, 600 )
            screen.blit(textInfoClear, textRectInfoClear)
            
            # Target Information
            if (i <= 2):
                textInfo = font.render(str(targetinfo[i])+' m', True, black, white)
            else:
                textInfo = font.render(str(targetinfo[i]), True, black, white)
            textRectInfo = textInfo.get_rect()
            if (i <= 2):
                textRectInfo.center = (X-330 +(i*200), 550 )
            elif (i == 3):
                textRectInfo.center = (X-320, 600 )
            elif (i == 4):
                textRectInfo.center = (X-140, 600 )
            elif (i == 5):
                textRectInfo.center = (X+75, 600 )
            screen.blit(textInfo, textRectInfo)
            
        pygame.display.update()
        pygame.display.flip()

        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            # exit the program
            if event.type == pygame.QUIT:
                is_running = False
                sys.exit()
            # click button
            if event.type == pygame.USEREVENT:
                # Joint 1
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == Reset_button:
                        print('Reset')
                        movement.setObjectInfo(int(hc.blueBlockHandle),float(hc.posX[0]),float(hc.posY[0]),float(hc.posZ[0]),float(hc.oriA[0]),float(hc.oriB[0]),float(hc.oriG[0]))
                        movement.setObjectInfo(int(hc.greenBlockHandle),float(hc.posX[1]),float(hc.posY[1]),float(hc.posZ[1]),float(hc.oriA[1]),float(hc.oriB[1]),float(hc.oriG[1]))
                        movement.setObjectInfo(int(hc.greenLakeBlockHandle),float(hc.posX[2]),float(hc.posY[2]),float(hc.posZ[2]),float(hc.oriA[2]),float(hc.oriB[2]),float(hc.oriG[2]))
                        movement.setObjectInfo(int(hc.purpleBlockHandle),float(hc.posX[3]),float(hc.posY[3]),float(hc.posZ[3]),float(hc.oriA[3]),float(hc.oriB[3]),float(hc.oriG[3]))
                        movement.setObjectInfo(int(hc.redBlockHandle),float(hc.posX[4]),float(hc.posY[4]),float(hc.posZ[4]),float(hc.oriA[4]),float(hc.oriB[4]),float(hc.oriG[4]))
                        movement.setObjectInfo(int(hc.whiteBlockHandle),float(hc.posX[5]),float(hc.posY[5]),float(hc.posZ[5]),float(hc.oriA[5]),float(hc.oriB[5]),float(hc.oriG[5]))
                        movement.setObjectInfo(int(hc.yellowBlockHandle),float(hc.posX[6]),float(hc.posY[6]),float(hc.posZ[6]),float(hc.oriA[6]),float(hc.oriB[6]),float(hc.oriG[6]))
                        robot.returnPose()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Add5_button:
                        print('Joint 1 Add 5!')
                        movement.rotateCertainAnglePositive(0,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Sub5_button:
                        print('Joint 1 Sub 5!')
                        movement.rotateCertainAngleNegative(0,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Add_button:
                        print('Joint 1 Add!')
                        movement.rotateCertainAnglePositive(0,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Sub_button:
                        print('Joint 1 Sub!')
                        movement.rotateCertainAngleNegative(0,1)
                # Joint 2
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Add5_button:
                        print('Joint 2 Add 5!')
                        movement.rotateCertainAnglePositive(1,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Sub5_button:
                        print('Joint 2 Sub 5!')
                        movement.rotateCertainAngleNegative(1,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Add_button:
                        print('Joint 2 Add!')
                        movement.rotateCertainAnglePositive(1,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Sub_button:
                        print('Joint 2 Sub!')
                        movement.rotateCertainAngleNegative(1,1)
                # Joint 3
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Add5_button:
                        print('Joint 3 Add 5!')
                        movement.rotateCertainAnglePositive(2,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Sub5_button:
                        print('Joint 3 Sub 5!')
                        movement.rotateCertainAngleNegative(2,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Add_button:
                        print('Joint 3 Add!')
                        movement.rotateCertainAnglePositive(2,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Sub_button:
                        print('Joint 3 Sub!')
                        movement.rotateCertainAngleNegative(2,1)
                # Joint 4
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Add5_button:
                        print('Joint 4 Add 5!')
                        movement.rotateCertainAnglePositive(3,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Sub5_button:
                        print('Joint 4 Sub 5!')
                        movement.rotateCertainAngleNegative(3,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Add_button:
                        print('Joint 4 Add!')
                        movement.rotateCertainAnglePositive(3,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Sub_button:
                        print('Joint 4 Sub!')
                        movement.rotateCertainAngleNegative(3,1)
                # Joint 5
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Add5_button:
                        print('Joint 5 Add 5!')
                        movement.rotateCertainAnglePositive(4,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Sub5_button:
                        print('Joint 5 Sub 5!')
                        movement.rotateCertainAngleNegative(4,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Add_button:
                        print('Joint 5 Add!')
                        movement.rotateCertainAnglePositive(4,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Sub_button:
                        print('Joint 5 Sub!')
                        movement.rotateCertainAngleNegative(4,1)
                # Joint 6
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Add5_button:
                        print('Joint 6 Add 5!')
                        movement.rotateCertainAnglePositive(5,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Sub5_button:
                        print('Joint 6 Sub 5!')
                        movement.rotateCertainAngleNegative(5,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Add_button:
                        print('Joint 6 Add!')
                        movement.rotateCertainAnglePositive(5,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Sub_button:
                        print('Joint 6 Sub!')
                        movement.rotateCertainAngleNegative(5,1)
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
                        active = True 
                        hc.functionStatus[0] = 1    
                        hc.question = "Please input the value of Base (Joint 1) in degree (deg): "   
                        hc.inputHeading = "Input: "
                        hc.setTargetStatus[0] = 1
                        print("Set Target Button is clicked!")
                        print("Current function status is: ", hc.functionStatus)
                        print("Current Set Target Status is: ",hc.setTargetStatus)

            manager.process_events(event)
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                '''
                if(event.unicode == "\b"):
                    print("K_BACKSPACE")
                elif(event.unicode == "\r"):
                    print("K_RETURN")
                print(event.unicode)
                '''
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
    
                # Unicode standard is used for string
                # formation
                if event.key == pygame.K_RETURN:
                    # get and print the user inputed message.
                    questionTopicInfo = base_font.render("                                                                                                                          ", True, black, white)
                    questionTopic = pygame.Rect(25,700,700,32)
                    screen.blit(questionTopicInfo, questionTopic)
                    try:
                        userInputCheck = float(user_text)
                        if(user_text != ""):
                            print("The user input: ", user_text[:])
                            hc.userInput = user_text[:]
                            print("The value passed to the function")
                            for i in range(len(hc.functionStatus)):
                                if(hc.functionStatus[i] == 1):
                                    print("Working with function ", int(i))
                                    if(int(i) == 0):							# Checking whether function1 (setTarget) is using
                                        #print(int(i) == 0)
                                        print(1 in hc.setTargetStatus)
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
                                                robot.setJointAngle()
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
                '''
                if event.key == pygame.K_p:
                    robot.StopSimulation()
                    sys.exit()
                # joinit 0
                elif event.key == pygame.K_q:
                    movement.rotateCertainAngleNegative(0, angle)
                elif event.key == pygame.K_w:
                    movement.rotateCertainAnglePositive(0, angle)
                # joinit 1
                elif event.key == pygame.K_a:
                    movement.rotateCertainAngleNegative(1, angle)
                elif event.key == pygame.K_s:
                    movement.rotateCertainAnglePositive(1, angle)
                # joinit 2
                elif event.key == pygame.K_z:
                    movement.rotateCertainAngleNegative(2, angle)
                elif event.key == pygame.K_x:
                    movement.rotateCertainAnglePositive(2, angle)
                # joinit 3
                elif event.key == pygame.K_e:
                    movement.rotateCertainAngleNegative(3, angle)
                elif event.key == pygame.K_r:
                    movement.rotateCertainAnglePositive(3, angle)
                # joinit 4
                elif event.key == pygame.K_d:
                    movement.rotateCertainAngleNegative(4, angle)
                elif event.key == pygame.K_f:
                    movement.rotateCertainAnglePositive(4, angle)
                # joinit 5
                elif event.key == pygame.K_c:
                    movement.rotateCertainAngleNegative(5, angle)
                elif event.key == pygame.K_v:
                    movement.rotateCertainAnglePositive(5, angle)
                # close RG2
                elif event.key == pygame.K_t:
                    robot.closeRG2()
                # # open RG2
                elif event.key == pygame.K_y:
                    robot.openRG2()
                else:
                    print("Invalid input, no corresponding function for this key!")
                '''


        questionTopicInfo = base_font.render("------------------- User Input -------------------", True, blue, white)
        questionTopic = pygame.Rect(115,650,700,32)
        screen.blit(questionTopicInfo, questionTopic)

        questionTopicInfo = base_font.render(hc.question, True, black, white)
        questionTopic = pygame.Rect(25,700,700,32)
        screen.blit(questionTopicInfo, questionTopic)

        inputTopicInfo = base_font.render(hc.inputHeading, True, blue, white)
        inputTopic = pygame.Rect(240,750,50,32)
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
