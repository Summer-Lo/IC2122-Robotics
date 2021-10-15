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

class UR3_RG2:
    # variates
    resolutionX = 640               # Camera resolution: 640*480
    resolutionY = 680
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
        pos = [-3.8728e-01,-1.8161e-03,+1.1000e+00]
        ori = [-1.5952832962,0.092294756175,-0.017449452796]
        vrep.simxSetObjectPosition(clientID, targetHandle, -1, pos, vrep.simx_opmode_blocking)
        vrep.simxSetObjectOrientation(clientID, targetHandle, -1, ori, vrep.simx_opmode_blocking)



# control robot by keyboard
def main():
    robot = UR3_RG2()
    resolutionX = robot.resolutionX
    resolutionY = robot.resolutionY
    movement = Movement.Move()
    information = Information.data()
    
    #angle = float(eval(input("please input velocity: ")))
    angle = 1
    
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
    manager = pygame_gui.UIManager((800, 800))
    # Introd
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 25), (185, 45)),text='Adjusting Joint Angle',manager=manager)
    Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 25), (45, 45)),text='+5',manager=manager)
    Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 25), (45, 45)),text='-5',manager=manager)
    Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 25), (45, 45)),text='+1',manager=manager)
    Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 25), (45, 45)),text='-1',manager=manager)
    Status_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 25), (100, 45)),text='Disabled',manager=manager)
    # Joint 1 button
    joint1Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 75), (45, 45)),text='>>',manager=manager)
    joint1Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 75), (45, 45)),text='<<',manager=manager)
    joint1Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 75), (45, 45)),text='> (Q)',manager=manager)
    joint1Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 75), (45, 45)),text='(W) <',manager=manager)
    # Joint 2 button
    joint2Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 125), (45, 45)),text='>>',manager=manager)
    joint2Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 125), (45, 45)),text='<<',manager=manager)
    joint2Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 125), (45, 45)),text='> (A)',manager=manager)
    joint2Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 125), (45, 45)),text='(S) <',manager=manager)
    # Joint 3 button
    joint3Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 175), (45, 45)),text='>>',manager=manager)
    joint3Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 175), (45, 45)),text='<<',manager=manager)
    joint3Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 175), (45, 45)),text='> (Z)',manager=manager)
    joint3Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 175), (45, 45)),text='(X) <',manager=manager)
    # Joint 4 button
    joint4Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 225), (45, 45)),text='>>',manager=manager)
    joint4Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 225), (45, 45)),text='<<',manager=manager)
    joint4Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 225), (45, 45)),text='> (E)',manager=manager)
    joint4Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 225), (45, 45)),text='(R) <',manager=manager)
    # Joint 5 button
    joint5Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 275), (45, 45)),text='>>',manager=manager)
    joint5Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (45, 45)),text='<<',manager=manager)
    joint5Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (45, 45)),text='> (D)',manager=manager)
    joint5Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 275), (45, 45)),text='(F) <',manager=manager)
    # Joint 6 Button
    joint6Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 325), (45, 45)),text='>>',manager=manager)
    joint6Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 325), (45, 45)),text='<<',manager=manager)
    joint6Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 325), (45, 45)),text='> (C)',manager=manager)
    joint6Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 325), (45, 45)),text='(V) <',manager=manager)
    # Pose
    returnPose_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((75, 375), (150, 45)),text='Home Position (L)',manager=manager)
    openRG2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 375), (150, 45)),text='Open RG2 (Y)',manager=manager)
    closeRG2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((425, 375), (150, 45)),text='Close RG2 (T)',manager=manager) 
    # Set Position and Orientaiton
    setTarget_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((75, 575), (150, 45)),text='Set Target (I)',manager=manager) 
    setPosition_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 575), (150, 45)),text='Set Position (P)',manager=manager) 
    setOrientation_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((425, 575), (160, 45)),text='Set Orientation (O)',manager=manager)

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
            textInfoTopic = font.render('---End-Effector (Tip) Position and Orientation---', True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (300, 450 )
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
                # RG2
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == openRG2_button:
                        robot.openRG2()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == closeRG2_button:
                        robot.closeRG2()
                # Target Position and Orientation
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setTarget_button:
                        movement.setTarget()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setPosition_button:
                        movement.setTargetPosition()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setOrientation_button:
                        movement.setTargetOrientation()
                        
                     

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

