#-*- coding:utf-8 -*-


import sys
import math
import time
import pygame
import pygame_gui
import numpy as np
import subprocess
import os

# control robot by keyboard
def main():
    resolutionX = 200
    resolutionY = 700
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (68,28)
    pygame.init()
    screen = pygame.display.set_mode((resolutionX, resolutionY))
    screen.fill((255,255,255))
    pygame.display.set_caption("IC2122 Control Panel")
    # looping, can resume moving with pressing one key
    pygame.key.set_repeat(200,50)
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    black = (0, 0, 0)
    manager = pygame_gui.UIManager((200, 700))
    
    # Button for Task selection
    task1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 25), (100, 45)),text='Task 1',manager=manager)
    task1c_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 75), (100, 45)),text='Task 1C',manager=manager)

    task2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 175), (100, 45)),text='Task 2',manager=manager)
    task2c_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 225), (100, 45)),text='Task 2C',manager=manager)

    task3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 325), (100, 45)),text='Task 3',manager=manager)

    task4a_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 425), (100, 45)),text='Task 4A',manager=manager)
    task4b_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 475), (100, 45)),text='Task 4B',manager=manager)
    task4c_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 525), (100, 45)),text='Task 4C',manager=manager)

    ursim_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 625), (100, 45)),text='URSim',manager=manager)
    
    clock = pygame.time.Clock()
    # Configurating RG2
    
    while True:
        time_delta = clock.tick(60)/1000.0
        pygame.display.update()
        
        pygame.display.update()
        pygame.display.flip()

        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            # exit the program
            if event.type == pygame.QUIT:
                is_running = False
                sys.exit()

            # Task Button Control
            if event.type == pygame.USEREVENT:
            # Task 1
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == task1_button:
                        subprocess.call(['gnome-terminal', '--title=Task1', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task1.bash'])
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == task1c_button:
                        subprocess.call(['gnome-terminal', '--title=Task1c', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task1c.bash'])

            # Task 2
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == task2_button:
                        subprocess.call(['gnome-terminal', '--title=Task2', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task2.bash'])

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == task2c_button:
                        subprocess.call(['gnome-terminal', '--title=Task2c', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task2c.bash'])

            # Task 3
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == task3_button:
                        subprocess.call(['gnome-terminal', '--title=Task3', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task3.bash'])

            # Task 4
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == task4a_button:
                        subprocess.call(['gnome-terminal', '--title=Task4A', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4a.bash'])  

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == task4b_button:
                        subprocess.call(['gnome-terminal', '--title=Task4B', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4b.bash'])

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == task4c_button:
                        subprocess.call(['gnome-terminal', '--title=Task4C', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4c.bash'])           

            # URSim v5.12 in ubuntu
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == ursim_button:
                        subprocess.call(['gnome-terminal', '--title=URSim', '-x', '/home/topic2/Desktop/IC2122-Robotics/URSim.bash'])

            # Task Keyboard Control
            manager.process_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    sys.exit()

                # Task 1
                elif event.key == pygame.K_1:
                    subprocess.call(['gnome-terminal', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task1.bash'])
                elif event.key == pygame.K_q:
                    subprocess.call(['gnome-terminal', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task1c.bash'])
                
                # Task 2
                elif event.key == pygame.K_2:
                    subprocess.call(['gnome-terminal', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task2.bash'])                
                elif event.key == pygame.K_w:
                    subprocess.call(['gnome-terminal', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task2c.bash'])

                # Task 3
                elif event.key == pygame.K_3:
                    subprocess.call(['gnome-terminal', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task3.bash'])

                # Task 4
                elif event.key == pygame.K_4:
                    subprocess.call(['gnome-terminal', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4a.bash'])
                elif event.key == pygame.K_r:
                    subprocess.call(['gnome-terminal', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4b.bash'])
                elif event.key == pygame.K_f:
                    subprocess.call(['gnome-terminal', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4c.bash'])

                # URSim v5.12 in ubuntu
                elif event.key == pygame.K_5:
                    subprocess.call(['gnome-terminal', '--title=URSim', '-x', '/home/topic2/Desktop/IC2122-Robotics/URSim.bash'])
                else:
                    print("Invalid input, no corresponding function for this key!")


        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()
                    
if __name__ == '__main__':
    main()
