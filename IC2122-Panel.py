#-*- coding:utf-8 -*-


import sys
import math
import time
import pygame
import pygame_gui
import numpy as np
import subprocess
import os
<<<<<<< HEAD
import panel_config as hc
import threading

=======
>>>>>>> 3a5823afe8062df3d7f830df862802fd3ff1c098

# control robot by keyboard
def main():
    resolutionX = 200
    resolutionY = 800
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
    manager = pygame_gui.UIManager((200, 800))
    
    # Button for Task selection
<<<<<<< HEAD
    hc.labSim_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 25), (100, 45)),text='LabSim',manager=manager)
    hc.labSim_close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 25), (40, 45)),text='X',manager=manager)

    hc.task1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 125), (100, 45)),text='Task 1',manager=manager)
    hc.task1_close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 125), (40, 45)),text='X',manager=manager)
    hc.task1c_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 175), (100, 45)),text='Task 1C',manager=manager)
    hc.task1c_close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 175), (40, 45)),text='X',manager=manager)

    hc.task2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 275), (100, 45)),text='Task 2',manager=manager)
    hc.task2_close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 275), (40, 45)),text='X',manager=manager)
    hc.task2c_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 325), (100, 45)),text='Task 2C',manager=manager)
    hc.task2c_close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 325), (40, 45)),text='X',manager=manager)

    hc.task3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 425), (100, 45)),text='Task 3',manager=manager)
    hc.task3_close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 425), (40, 45)),text='X',manager=manager)

    hc.task4a_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 525), (100, 45)),text='Task 4A',manager=manager)
    hc.task4a_close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 525), (40, 45)),text='X',manager=manager)
    hc.task4b_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 575), (100, 45)),text='Task 4B',manager=manager)
    hc.task4b_close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 575), (40, 45)),text='X',manager=manager)
    hc.task4c_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 625), (100, 45)),text='Task 4C',manager=manager)
    hc.task4c_close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 625), (40, 45)),text='X',manager=manager)

    hc.ursim_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 725), (100, 45)),text='URSim',manager=manager)
    hc.ursim_close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 725), (40, 45)),text='X',manager=manager)
    
    clock = pygame.time.Clock()
    # Configurating RG2

    hc.disableCloseButton()
=======
    labSim_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 25), (100, 45)),text='LabSim',manager=manager)

    task1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 125), (100, 45)),text='Task 1',manager=manager)
    task1c_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 175), (100, 45)),text='Task 1C',manager=manager)

    task2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 275), (100, 45)),text='Task 2',manager=manager)
    task2c_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 325), (100, 45)),text='Task 2C',manager=manager)

    task3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 425), (100, 45)),text='Task 3',manager=manager)

    task4a_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 525), (100, 45)),text='Task 4A',manager=manager)
    task4b_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 575), (100, 45)),text='Task 4B',manager=manager)
    task4c_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 625), (100, 45)),text='Task 4C',manager=manager)

    ursim_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 725), (100, 45)),text='URSim',manager=manager)
    
    clock = pygame.time.Clock()
    # Configurating RG2
>>>>>>> 3a5823afe8062df3d7f830df862802fd3ff1c098
    
    while True:
        time_delta = clock.tick(60)/1000.0
        pygame.display.update()
        
        pygame.display.update()
        pygame.display.flip()

<<<<<<< HEAD

=======
>>>>>>> 3a5823afe8062df3d7f830df862802fd3ff1c098
        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            # exit the program
            if event.type == pygame.QUIT:
                is_running = False
                sys.exit()

            # Task Button Control
            if event.type == pygame.USEREVENT:
            # LabSim
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
<<<<<<< HEAD
                    if event.ui_element == hc.labSim_button:
                        subprocess.call(['gnome-terminal', '--title=LabSim', '-x', '/home/topic2/Desktop/IC2122-Robotics/LabSim.bash'])
                        hc.disableButton()
                        enableClose1 = threading.Thread(target=hc.enableCloseButton, args=(1,))
                        enableClose1.start()

                    if event.ui_element == hc.labSim_close_button:
                        hc.enableButton()
                        hc.disableCloseButton()
                        os.system("kill $(pgrep -f vrep)")
                        enableClose1.join()

            # Task 1
                    if event.ui_element == hc.task1_button:
                        subprocess.call(['gnome-terminal', '--title=Task1', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task1.bash'])
                        hc.disableButton()
                        enableClose2 = threading.Thread(target=hc.enableCloseButton, args=(2,))
                        enableClose2.start()

                    if event.ui_element == hc.task1_close_button:
                        hc.enableButton()
                        hc.disableCloseButton()
                        os.system("kill $(pgrep -f Task1.py)")
                        enableClose2.join()

                    if event.ui_element == hc.task1c_button:
                        subprocess.call(['gnome-terminal', '--title=Task1c', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task1c.bash'])
                        hc.disableButton()
                        enableClose3 = threading.Thread(target=hc.enableCloseButton, args=(3,))
                        enableClose3.start()

                    if event.ui_element == hc.task1c_close_button:
                        hc.enableButton()
                        hc.disableCloseButton()
                        os.system("kill $(pgrep -f Task1.py)")
                        enableClose3.join()

            # Task 2

                    if event.ui_element == hc.task2_button:
                        subprocess.call(['gnome-terminal', '--title=Task2', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task2.bash'])
                        hc.disableButton()
                        enableClose4 = threading.Thread(target=hc.enableCloseButton, args=(4,))
                        enableClose4.start()

                    if event.ui_element == hc.task2_close_button:
                        hc.enableButton()
                        hc.disableCloseButton()
                        os.system("kill $(pgrep -f Task2.py)")
                        enableClose4.join()


                    if event.ui_element == hc.task2c_button:
                        subprocess.call(['gnome-terminal', '--title=Task2c', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task2c.bash'])
                        hc.disableButton()
                        enableClose5 = threading.Thread(target=hc.enableCloseButton, args=(5,))
                        enableClose5.start()

                    if event.ui_element == hc.task2c_close_button:
                        hc.enableButton()
                        hc.disableCloseButton()
                        os.system("kill $(pgrep -f Task2c.py)")
                        enableClose5.join()

            # Task 3

                    if event.ui_element == hc.task3_button:
                        subprocess.call(['gnome-terminal', '--title=Task3', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task3.bash'])
                        hc.disableButton()
                        enableClose6 = threading.Thread(target=hc.enableCloseButton, args=(6,))
                        enableClose6.start()

                    if event.ui_element == hc.task3_close_button:
                        hc.enableButton()
                        hc.disableCloseButton()
                        os.system("kill $(pgrep -f Task3.py)")
                        enableClose6.join()

            # Task 4

                    if event.ui_element == hc.task4a_button:
                        subprocess.call(['gnome-terminal', '--title=Task4A', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4a.bash'])  
                        hc.disableButton()
                        enableClose7 = threading.Thread(target=hc.enableCloseButton, args=(7,))
                        enableClose7.start()

                    if event.ui_element == hc.task4a_close_button:
                        hc.enableButton()
                        hc.disableCloseButton()
                        os.system("kill $(pgrep -f Task4.py)")
                        enableClose7.join()

                    if event.ui_element == hc.task4b_button:
                        subprocess.call(['gnome-terminal', '--title=Task4B', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4b.bash'])
                        hc.disableButton()
                        enableClose8 = threading.Thread(target=hc.enableCloseButton, args=(8,))
                        enableClose8.start()

                    if event.ui_element == hc.task4b_close_button:
                        hc.enableButton()
                        hc.disableCloseButton()
                        os.system("kill $(pgrep -f Task4.py)")
                        enableClose8.join()


                    if event.ui_element == hc.task4c_button:
                        subprocess.call(['gnome-terminal', '--title=Task4C', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4c.bash'])
                        hc.disableButton() 
                        enableClose9 = threading.Thread(target=hc.enableCloseButton, args=(9,)) 
                        enableClose9.start()  

                    if event.ui_element == hc.task4c_close_button:
                        hc.enableButton()  
                        hc.disableCloseButton() 
                        os.system("kill $(pgrep -f Task4.py)")    
                        enableClose9.join()

            # URSim v5.12 in ubuntu

                    if event.ui_element == hc.ursim_button:
                        subprocess.call(['gnome-terminal', '--title=URSim', '-x', '/home/topic2/Desktop/IC2122-Robotics/URSim.bash'])
                        hc.disableButton()
                        enableClose10 = threading.Thread(target=hc.enableCloseButton, args=(10,))
                        enableClose10.start()

                    if event.ui_element == hc.ursim_close_button:
                        hc.enableButton()
                        hc.disableCloseButton()
                        os.system("kill $(pgrep -f ursim)")  
                        enableClose10.join()  
=======
                    if event.ui_element == labSim_button:
                        subprocess.call(['gnome-terminal', '--title=Task1', '-x', '/home/topic2/IC2122-Robotics/LabSim.bash'])

            # Task 1
                    if event.ui_element == task1_button:
                        subprocess.call(['gnome-terminal', '--title=Task1', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task1.bash'])

                    if event.ui_element == task1c_button:
                        subprocess.call(['gnome-terminal', '--title=Task1c', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task1c.bash'])

            # Task 2

                    if event.ui_element == task2_button:
                        subprocess.call(['gnome-terminal', '--title=Task2', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task2.bash'])


                    if event.ui_element == task2c_button:
                        subprocess.call(['gnome-terminal', '--title=Task2c', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task2c.bash'])

            # Task 3

                    if event.ui_element == task3_button:
                        subprocess.call(['gnome-terminal', '--title=Task3', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task3.bash'])

            # Task 4

                    if event.ui_element == task4a_button:
                        subprocess.call(['gnome-terminal', '--title=Task4A', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4a.bash'])  


                    if event.ui_element == task4b_button:
                        subprocess.call(['gnome-terminal', '--title=Task4B', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4b.bash'])


                    if event.ui_element == task4c_button:
                        subprocess.call(['gnome-terminal', '--title=Task4C', '-x', '/home/topic2/Desktop/IC2122-Robotics/Task4c.bash'])           

            # URSim v5.12 in ubuntu

                    if event.ui_element == ursim_button:
                        subprocess.call(['gnome-terminal', '--title=URSim', '-x', '/home/topic2/Desktop/IC2122-Robotics/URSim.bash'])
>>>>>>> 3a5823afe8062df3d7f830df862802fd3ff1c098

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
